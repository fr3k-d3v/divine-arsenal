"""Loopback-only Divine Arsenal adapter for the independent URE HTTP API."""
from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response
import os
import tempfile
import urllib.parse
from pydantic import BaseModel, ConfigDict, Field, field_validator

from . import notebook, rea_client

router = APIRouter(prefix="/api/rea", tags=["local-rea"])

PROFILE_ADAPTER_PREFIXES = {
    "identify": "identify@",
    "elf": "elf.metadata@",
    "ghidra": "ghidra.decompile@",
    "jadx": "jadx.decompile@",
    "binwalk": "binwalk.scan@",
    "radare2": "radare2.analyze@",
    "unblob": "unblob.scan@",
    "kaitai": "kaitai.dex@",
    "pdf": "pdf.metadata@",
    "tei": "tei.validate@",
    "iiif": "iiif.manifest@",
    "image": "image.metadata@",
    "grid": "grid.inspect@",
    "video": "rea.video@",
}
PROFILE_LABELS = {
    "identify": "Identify format and hash",
    "elf": "ELF structural metadata",
    "ghidra": "Ghidra static decompilation",
    "jadx": "JADX Android static decompilation",
    "binwalk": "Binwalk firmware signature scan",
    "radare2": "radare2 static analysis",
    "unblob": "Unblob chunk identification",
    "kaitai": "Kaitai DEX structural parse",
    "pdf": "PDF lexical metadata",
    "tei": "TEI XML structure validation",
    "iiif": "IIIF Presentation manifest validation",
    "image": "PNG/JPEG/TIFF header metadata",
    "grid": "CSV/TSV structure inspection",
    "video": "REA Video shot-by-shot forensics",
}
FORMAT_PROFILES = {
    "elf": ("identify", "elf", "ghidra", "radare2", "binwalk", "unblob"),
    "apk": ("identify", "jadx", "binwalk", "unblob"),
    "dex": ("identify", "kaitai", "jadx"),
    "java_class": ("identify", "jadx"),
    "android_boot": ("identify", "binwalk", "unblob"),
    "zip": ("identify", "binwalk", "unblob"),
    "unknown": ("identify", "binwalk", "unblob"),
    "pe": ("identify", "binwalk", "unblob"),
    "pcap": ("identify",),
    "text": ("identify",),
    "json": ("identify",),
    "pdf": ("identify", "pdf"),
    "tei_xml": ("identify", "tei"),
    "iiif_manifest": ("identify", "iiif"),
    "image.png": ("identify", "image"),
    "image.jpeg": ("identify", "image"),
    "image.tiff": ("identify", "image"),
    "grid.csv": ("identify", "grid"),
    "grid.tsv": ("identify", "grid"),
    "video.mp4": ("identify", "video"),
    "video.mov": ("identify", "video"),
    "video.mkv": ("identify", "video"),
    "video.webm": ("identify", "video"),
    "video.avi": ("identify", "video"),
}


class UploadRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    filename: str = Field(min_length=1, max_length=255)
    content_base64: str = Field(min_length=4, max_length=933_336)

    @field_validator("filename")
    @classmethod
    def safe_filename(cls, value):
        if (value in (".", "..") or value != value.strip()
                or "/" in value or "\\" in value
                or any(ord(char) < 32 or ord(char) == 127 for char in value)):
            raise ValueError("Filename must be a plain file name without path components")
        return value


class JobRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    input_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    profile: Literal["identify", "elf", "ghidra", "jadx", "binwalk", "radare2", "unblob", "kaitai", "pdf", "tei", "iiif", "image", "grid", "video"]


class NotebookReferenceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    source_id: str | None = Field(default=None, min_length=2, max_length=80)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    note: str = Field(default="", max_length=5000)


def _raise(error):
    if isinstance(error, rea_client.REAError):
        raise HTTPException(error.http_status, error.public_detail) from error
    if isinstance(error, ValueError):
        raise HTTPException(422, "Invalid REA request") from error
    raise HTTPException(503, rea_client.REAUnavailable.public_detail) from error


def _ready_status():
    current = rea_client.status()
    if current.get("status") != "READY":
        detail = current.get("message") or rea_client.REAUnavailable.public_detail
        raise HTTPException(503, detail)
    return current


def _adapter_for(profile, adapters):
    prefix = PROFILE_ADAPTER_PREFIXES[profile]
    candidates = [item for item in adapters if
        isinstance(item.get("identity"), str) and item["identity"].startswith(prefix)
        and item.get("available") is True and item.get("enabled") is True
        and item.get("verified") is True and item.get("status") == "SUPPORTED"]
    if not candidates:
        return None
    def version_key(item):
        import re
        match = re.search(r"@(\d+)\.(\d+)\.(\d+)$", item["identity"])
        return tuple(int(part) for part in match.groups()) if match else (0, 0, 0)
    return max(candidates, key=version_key)["identity"]


def _suggestions(file_format, adapters):
    profiles = FORMAT_PROFILES.get(file_format, ("identify",))
    result = []
    for profile in profiles:
        identity = _adapter_for(profile, adapters)
        if identity is None:
            continue
        result.append({
            "profile": profile, "adapter": identity,
            "label": PROFILE_LABELS[profile], "authority": "OBSERVE",
        })
    return result


@router.get("/status")
def status():
    return rea_client.status()


@router.get("/adapters")
def adapters():
    current = _ready_status()
    return {"adapters": current["adapters"], "worker": current["worker"]}


@router.post("/inputs", status_code=201)
def upload(data: UploadRequest):
    current = _ready_status()
    try:
        item = rea_client.upload_base64(data.filename, data.content_base64)
    except Exception as error:
        _raise(error)
    return {
        "input": item,
        "suggested_profiles": _suggestions(item["classification"]["format"], current["adapters"]),
        "authority": "OBSERVE",
        "limitations": [
            "Standard artifacts are limited to 700,000 bytes through JSON intake; video has a dedicated raw streaming route capped at 64 MiB.",
            "Video analysis is a separate pinned, offline REA Video worker. VLM/OCR/HTR/ASR and source separation are disabled by default.",
            "Classification is signature-based. PDF/image/OCR/HTR interpretation is not implied.",
            "The original is stored by the local URE evidence service; Divine Arsenal does not copy it into its repository.",
        ],
    }


@router.post("/inputs/video", status_code=201)
async def upload_video(request: Request):
    current = _ready_status()
    if request.headers.get("content-type","").split(";",1)[0].strip().lower() != "application/octet-stream":
        raise HTTPException(415,"Use application/octet-stream for local video intake")
    raw_name=request.headers.get("x-file-name","")
    try:
        filename=urllib.parse.unquote(raw_name,errors="strict")
    except (UnicodeError,ValueError):
        raise HTTPException(422,"Invalid video filename")
    if (not 1<=len(filename)<=255 or filename in (".","..") or filename!=filename.strip()
        or "/" in filename or chr(92) in filename
        or any(ord(char)<32 or ord(char)==127 for char in filename)):
        raise HTTPException(422,"Video filename must be a plain file name")
    try:
        expected=int(request.headers.get("content-length",""))
    except ValueError:
        raise HTTPException(411,"Content-Length is required")
    if expected<1:
        raise HTTPException(400,"Empty video upload")
    if expected>64*1024*1024:
        raise HTTPException(413,"Video exceeds the 64 MiB local intake limit")
    descriptor,temporary=tempfile.mkstemp(prefix="divine-rea-video-")
    os.fchmod(descriptor,0o600)
    size=0
    try:
        with os.fdopen(descriptor,"wb") as destination:
            async for chunk in request.stream():
                size+=len(chunk)
                if size>64*1024*1024:
                    raise HTTPException(413,"Video exceeds the 64 MiB local intake limit")
                destination.write(chunk)
            destination.flush()
            os.fsync(destination.fileno())
        if size!=expected:
            raise HTTPException(400,"Video upload length mismatch")
        item=rea_client.upload_video_file(temporary,filename)
    except Exception as error:
        if isinstance(error,HTTPException):
            raise
        _raise(error)
    finally:
        try:os.unlink(temporary)
        except FileNotFoundError:pass
    return {
        "input":item,
        "suggested_profiles":_suggestions(item["classification"]["format"],current["adapters"]),
        "authority":"OBSERVE",
        "limitations":[
            "Local video intake is capped at 64 MiB and uses a separate raw streaming route.",
            "The pinned rea-video worker runs offline in Bubblewrap; VLM, OCR/HTR, ASR, speaker separation and stems are disabled.",
            "Shot production-method labels are provisional until an agent or human reviews the generated storyboard and review tasks.",
            "The original video is content-addressed in the local URE evidence store; no cloud upload or source-video modification occurs.",
        ],
    }


@router.post("/jobs", status_code=202)
def create_job(data: JobRequest):
    current = _ready_status()
    adapter = _adapter_for(data.profile, current["adapters"])
    if adapter is None:
        raise HTTPException(409, "Selected profile has no currently verified, enabled adapter")
    try:
        return rea_client.create_job(data.input_sha256, data.profile, adapter)
    except Exception as error:
        _raise(error)


@router.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        return rea_client.get_job(job_id)
    except Exception as error:
        _raise(error)


def _job_report(job_id: str):
    current = _ready_status()
    job = rea_client.get_job(job_id)
    descriptor = next((item for item in current["adapters"] if item.get("identity") == job.get("adapter")), None)
    report = rea_client.get_report(job_id, job, descriptor)
    input_hashes = {item["sha256"] for item in report["analysis"]["inputs"]}
    if job.get("input_sha256") not in input_hashes:
        raise rea_client.REAProtocolError("job_report_input_mismatch")
    return job, report


@router.get("/jobs/{job_id}/report")
def get_report(job_id: str):
    try:
        _, report = _job_report(job_id)
        return report
    except Exception as error:
        _raise(error)


@router.get("/jobs/{job_id}/artifacts")
def get_artifacts(job_id: str):
    try:
        return rea_client.get_artifacts(job_id)
    except Exception as error:
        _raise(error)


@router.get("/jobs/{job_id}/artifacts/{name}")
def get_artifact(job_id: str, name: str):
    try:
        item=rea_client.get_artifact(job_id,name)
        headers={"X-Content-Type-Options":"nosniff","Cache-Control":"no-store"}
        if name=="report.html":
            headers["Content-Disposition"]='attachment; filename="report.html"'
            headers["Content-Security-Policy"]="sandbox; default-src 'none'; img-src data:; style-src 'unsafe-inline'; font-src data:"
        elif name in ("storyboard.jpg","audio.png"):
            headers["Content-Disposition"]=f'inline; filename="{name}"'
        else:
            headers["Content-Disposition"]=f'attachment; filename="{name}"'
        return Response(content=item["data"],media_type=item["content_type"],headers=headers)
    except Exception as error:
        _raise(error)


@router.post("/jobs/{job_id}/notebook", status_code=201)
def save_notebook_reference(job_id: str, data: NotebookReferenceRequest):
    try:
        job, report = _job_report(job_id)
        if job.get("state") != "succeeded":
            raise HTTPException(409, "Only completed analysis jobs can be saved as notebook evidence")
        for row in notebook.listing("analysis-reference"):
            existing = notebook.get(row["id"])
            if existing and existing["document"].get("job_id") == job_id:
                return {"id": row["id"], "revision": existing["revision"], "existing": True}
        analysis = report["analysis"]
        execution = analysis["execution_summary"]
        resource_limits = analysis.get("resource_limits", {})
        # Multiple streams can contain identical bytes (for example, empty stdout and stderr).
        # Keep every raw evidence record in the report, but store unique content hashes in the notebook.
        evidence_hashes = list(dict.fromkeys(item["sha256"] for item in analysis["evidence"]))
        title = data.title or f"REA · {job['adapter']} · {job['input_sha256'][:12]}"
        document = notebook.AnalysisReference.model_validate({
            "kind": "analysis-reference", "title": title,
            "job_id": job_id, "input_sha256": job["input_sha256"],
            "adapter": job["adapter"], "profile": job["profile"],
            "authority": execution["authority"], "state": job["state"],
            "created_at": execution.get("created_at"),
            "started_at": execution.get("started_at"),
            "finished_at": execution.get("finished_at"),
            "attempt_count": execution.get("attempt_count", 1),
            "sandbox_profile": execution.get("sandbox_profile", "UNKNOWN"),
            "network_policy": execution.get("network_policy", "UNKNOWN"),
            "filesystem_policy": execution.get("filesystem_policy", "UNKNOWN"),
            "permissions": execution.get("permissions", ["OBSERVE"]),
            "resource_limits": resource_limits,
            "exit_code": execution.get("exit_code"),
            "timed_out": execution.get("timed_out", False),
            "truncated": execution.get("truncated", False),
            "cancelled": execution.get("cancelled", False),
            "reaped": execution.get("reaped", False),
            "error": execution.get("error"),
            "evidence_hashes": evidence_hashes,
            "artifacts": analysis.get("artifacts", []),
            "findings": analysis["findings"],
            "reconstructions": analysis["reconstructions"],
            "limitations": analysis["limitations"],
            "provider_limitations": analysis["provider_limitations"],
            "compatibility_notes": analysis["compatibility_notes"],
            "source_id": data.source_id, "note": data.note,
        })
        saved = notebook.save(notebook.Save(expected_revision=0, document=document))
        return {"id": saved["id"], "revision": saved["revision"], "existing": False}
    except HTTPException:
        raise
    except Exception as error:
        _raise(error)


@router.post("/jobs/{job_id}/cancel")
def cancel_job(job_id: str):
    try:
        return rea_client.cancel_job(job_id)
    except Exception as error:
        _raise(error)
