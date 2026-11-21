"""Strict HTTP-only client for the local Universal Reverse Engineering service.

Divine Arsenal never imports URE internals, launches analyzers, or receives URE
fencing tokens. All calls are loopback-only and reports are reduced to a safe
evidence envelope before reaching the browser.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import ipaddress
import json
import math
import os
import re
import urllib.error
import urllib.parse
import urllib.request

MAX_UPLOAD_BYTES = 700_000
MAX_VIDEO_BYTES = 64 * 1024 * 1024
MAX_ARTIFACT_BYTES = 16 * 1024 * 1024
MAX_RESPONSE_BYTES = 4 * 1024 * 1024
PROFILES = frozenset({
    "identify", "elf", "ghidra", "jadx", "binwalk", "radare2", "unblob", "kaitai",
    "pdf", "tei", "iiif", "image", "grid", "video",
})
JOB_STATES = frozenset({
    "queued", "running", "succeeded", "failed", "timed_out", "cancelled", "blocked"
})
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
JOB_ID_RE = re.compile(r"^[0-9a-f]{32}$")


class REAError(Exception):
    http_status = 503
    public_detail = "The local REA service is unavailable."


class REAConfigurationError(REAError):
    public_detail = "REA is not configured. Set URE_URL and URE_API_TOKEN for the Divine Arsenal process."


class REAUnavailable(REAError):
    public_detail = "The local REA service did not respond or rejected the connection."


class REAAuthenticationError(REAError):
    public_detail = "The local REA service rejected its configured authentication token."


class REAPolicyError(REAError):
    http_status = 409
    public_detail = "The requested REA operation is not permitted."


class REAConflict(REAError):
    http_status = 409
    public_detail = "The REA job conflicts with an existing idempotency record."


class REANotFound(REAError):
    http_status = 404
    public_detail = "The requested REA job or input was not found."


class REAInvalid(REAError):
    http_status = 422
    public_detail = "The REA service rejected the request."


class REATooLarge(REAError):
    http_status = 413
    public_detail = "The artifact exceeds the current Divine-to-REA upload limit."


class REAProtocolError(REAError):
    http_status = 502
    public_detail = "The REA service returned an invalid response."


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        raise ValueError("redirect_denied")


def _settings():
    url = os.environ.get("URE_URL", "http://127.0.0.1:18879").strip()
    token = os.environ.get("URE_API_TOKEN", "")
    if len(token.encode("utf-8")) < 32:
        raise REAConfigurationError("not_configured")
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != "http" or parsed.username or parsed.password
            or parsed.path not in ("", "/") or parsed.query or parsed.fragment
            or parsed.hostname != "127.0.0.1" or parsed.port is None
            or not 1 <= parsed.port <= 65535):
        raise REAConfigurationError("loopback_url_required")
    try:
        address = ipaddress.ip_address(parsed.hostname)
    except ValueError as error:
        raise REAConfigurationError("numeric_loopback_required") from error
    if not address.is_loopback or address.version != 4:
        raise REAConfigurationError("ipv4_loopback_required")
    try:
        timeout = float(os.environ.get("URE_TIMEOUT", "10"))
    except ValueError as error:
        raise REAConfigurationError("invalid_timeout") from error
    if not math.isfinite(timeout) or not 0 < timeout <= 30:
        raise REAConfigurationError("invalid_timeout")
    return url.rstrip("/"), token, timeout, parsed.port


def _decode_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate_json_key")
            result[key] = value
        return result

    def constant(_value):
        raise ValueError("nonfinite_json")

    try:
        value = json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, UnicodeError, RecursionError) as error:
        raise REAProtocolError("invalid_json") from error
    if not isinstance(value, (dict, list)):
        raise REAProtocolError("json_object_or_array_required")
    return value


def _request(path, method="GET", payload=None):
    base, token, timeout, _port = _settings()
    if not path.startswith("/v1/") or "?" in path or "#" in path:
        raise REAProtocolError("invalid_internal_path")
    body = None if payload is None else json.dumps(
        payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + token,
        "User-Agent": "DivineArsenal-Local-REA/1",
    }
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(base + path, data=body, headers=headers, method=method)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect())
    try:
        with opener.open(request, timeout=timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise REAProtocolError("response_too_large")
            return _decode_json(raw)
    except urllib.error.HTTPError as error:
        if error.code == 401:
            raise REAAuthenticationError("authentication_rejected") from error
        if error.code == 403:
            raise REAPolicyError("authority_denied") from error
        if error.code == 404:
            raise REANotFound("not_found") from error
        if error.code == 409:
            raise REAConflict("conflict") from error
        if error.code == 413:
            raise REATooLarge("body_too_large") from error
        if error.code == 400:
            raise REAInvalid("invalid_request") from error
        if error.code == 422:
            raise REAInvalid("invalid_request") from error
        raise REAUnavailable("http_error") from error
    except REAError:
        raise
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
        raise REAUnavailable("connection_failed") from error


def _safe_adapter(item):
    if not isinstance(item, dict) or not isinstance(item.get("identity"), str):
        return None
    safe = {"identity": item["identity"]}
    for key in ("name", "version", "status", "required_authority"):
        value = item.get(key)
        if isinstance(value, str):
            safe[key] = value[:160]
    for key in ("formats", "capabilities", "limitations"):
        value = item.get(key)
        if isinstance(value, list) and len(value) <= 64 and all(isinstance(x, str) for x in value):
            safe[key] = [x[:300] for x in value]
    for key in ("available", "installed", "verified", "enabled"):
        safe[key] = item.get(key) is True
    limits = {}
    for key, low, high in (("memory_mb", 1, 8192), ("cpu_seconds", 1, 120),
                           ("wall_seconds", 1, 180), ("output_bytes", 1, 4 * 1024 * 1024)):
        value = item.get(key)
        if type(value) is int and low <= value <= high:
            limits[key] = value
    safe["resource_limits"] = limits
    return safe


def status():
    try:
        base, _token, _timeout, port = _settings()
    except REAConfigurationError:
        return {
            "configured": False, "status": "NOT_CONFIGURED", "endpoint": None,
            "api_version": None, "adapters": [], "worker": {},
            "message": REAConfigurationError.public_detail,
        }
    try:
        health = _request("/v1/health")
        if not isinstance(health, dict) or health.get("status") != "ok" or type(health.get("schema_version")) is not int:
            raise REAProtocolError("health_schema")
        raw_adapters = _request("/v1/adapters")
        raw_workers = _request("/v1/workers")
        if not isinstance(raw_adapters, list) or not isinstance(raw_workers, dict):
            raise REAProtocolError("capability_schema")
        adapters = [item for item in (_safe_adapter(x) for x in raw_adapters) if item]
        caps = raw_workers.get("capabilities", {})
        if not isinstance(caps, dict):
            caps = {}
        worker = {
            "architecture": caps.get("architecture") if isinstance(caps.get("architecture"), str) else "UNKNOWN",
            "memory_mb": caps.get("memory_mb") if type(caps.get("memory_mb")) is int else None,
            "cpu": caps.get("cpu") if type(caps.get("cpu")) is int else None,
        }
        video = raw_workers.get("rea_video")
        if isinstance(video, dict):
            capsule = video.get("capsule_cinema", {})
            if not isinstance(capsule, dict):
                capsule = {}
            worker["rea_video"] = {
                "verified": video.get("verified") is True,
                "enabled": video.get("enabled") is True,
                "version": video.get("version") if isinstance(video.get("version"), str) else "UNKNOWN",
                "commit": video.get("commit") if isinstance(video.get("commit"), str) else None,
                "remake_plan": video.get("remake_plan") if video.get("remake_plan") in ("AVAILABLE","UNAVAILABLE") else "UNKNOWN",
                "generation_execution": video.get("generation_execution") if video.get("generation_execution") in ("BLOCKED_NO_RUNTIME","BLOCKED_NO_PROVIDER_CONFIG","APPROVAL_REQUIRED") else "UNKNOWN",
                "capsule_cinema": {
                    "verified": capsule.get("verified") is True,
                    "commit": capsule.get("commit") if isinstance(capsule.get("commit"), str) else None,
                    "generation_runtime_ready": capsule.get("generation_runtime_ready") is True,
                    "provider_config_file_present": capsule.get("provider_config_file_present") is True,
                    "license": capsule.get("license") is True,
                    "reason": capsule.get("reason") if isinstance(capsule.get("reason"), str) else "UNKNOWN",
                },
            }
        return {
            "configured": True, "status": "READY", "endpoint": f"127.0.0.1:{port}",
            "api_version": health["schema_version"], "adapters": adapters,
            "worker": worker, "message": "Authenticated local REA API available.",
        }
    except REAError:
        return {
            "configured": True, "status": "UNAVAILABLE", "endpoint": f"127.0.0.1:{port}",
            "api_version": None, "adapters": [], "worker": {},
            "message": REAUnavailable.public_detail,
        }


def _valid_filename(filename):
    return (
        isinstance(filename, str) and 1 <= len(filename) <= 255
        and filename not in (".", "..") and filename == filename.strip()
        and "/" not in filename and "\\" not in filename
        and not any(ord(char) < 32 or ord(char) == 127 for char in filename)
    )


def upload_base64(filename, content_base64):
    if not _valid_filename(filename):
        raise ValueError("invalid_filename")
    if not isinstance(content_base64, str) or len(content_base64) > 933_336:
        raise REATooLarge("encoded_input_too_large")
    try:
        content = base64.b64decode(content_base64, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ValueError("invalid_base64") from error
    if not content:
        raise ValueError("empty_input")
    if len(content) > MAX_UPLOAD_BYTES:
        raise REATooLarge("input_too_large")
    expected_sha = hashlib.sha256(content).hexdigest()
    descriptor = _request("/v1/inputs", "POST", {
        "filename": filename,
        "content_base64": base64.b64encode(content).decode("ascii"),
        "provenance": "divine-arsenal-local-research",
    })
    if (not isinstance(descriptor, dict) or descriptor.get("sha256") != expected_sha
            or descriptor.get("size") != len(content)
            or not isinstance(descriptor.get("classification"), dict)):
        raise REAProtocolError("input_descriptor_mismatch")
    classification = descriptor["classification"]
    if not isinstance(classification.get("format"), str):
        raise REAProtocolError("classification_schema")
    return {
        "sha256": expected_sha, "size": len(content), "filename": filename,
        "classification": classification,
    }


def upload_video_file(path, filename):
    if not _valid_filename(filename):
        raise ValueError("invalid_filename")
    if not isinstance(path,str) or not os.path.isabs(path) or os.path.islink(path):
        raise ValueError("invalid_video_path")
    info=os.stat(path,follow_symlinks=False)
    if not os.path.isfile(path) or info.st_size<1:
        raise ValueError("invalid_video_file")
    if info.st_size>MAX_VIDEO_BYTES:
        raise REATooLarge("video_input_too_large")
    digest=hashlib.sha256()
    with open(path,"rb") as source:
        for chunk in iter(lambda:source.read(1024*1024),b""):
            digest.update(chunk)
    expected_sha=digest.hexdigest()
    base,token,_timeout,_port=_settings()
    headers={
        "Accept":"application/json",
        "Authorization":"Bearer "+token,
        "User-Agent":"DivineArsenal-Local-REA/1",
        "Content-Type":"application/octet-stream",
        "Content-Length":str(info.st_size),
        "X-File-Name":urllib.parse.quote(filename,safe=""),
    }
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),_NoRedirect())
    try:
        with open(path,"rb") as source:
            request=urllib.request.Request(base+"/v1/inputs/video",data=source,headers=headers,method="POST")
            with opener.open(request,timeout=120) as response:
                raw=response.read(MAX_RESPONSE_BYTES+1)
                if len(raw)>MAX_RESPONSE_BYTES:raise REAProtocolError("response_too_large")
                descriptor=_decode_json(raw)
    except urllib.error.HTTPError as error:
        if error.code==401:raise REAAuthenticationError("authentication_rejected") from error
        if error.code==403:raise REAPolicyError("authority_denied") from error
        if error.code==413:raise REATooLarge("video_body_too_large") from error
        if error.code in (400,422):raise REAInvalid("invalid_video") from error
        raise REAUnavailable("video_upload_http_error") from error
    except REAError:
        raise
    except (urllib.error.URLError,TimeoutError,OSError,ValueError) as error:
        raise REAUnavailable("video_upload_failed") from error
    if (not isinstance(descriptor,dict) or descriptor.get("sha256")!=expected_sha
        or descriptor.get("size")!=info.st_size or not isinstance(descriptor.get("classification"),dict)
        or descriptor["classification"].get("format") not in ("video.mp4","video.mov","video.mkv","video.webm","video.avi")):
        raise REAProtocolError("video_input_descriptor_mismatch")
    return {"sha256":expected_sha,"size":info.st_size,"filename":filename,
            "classification":descriptor["classification"]}


def create_job(input_sha256, profile, adapter_identity):
    if not isinstance(input_sha256, str) or SHA256_RE.fullmatch(input_sha256) is None:
        raise ValueError("invalid_sha256")
    if profile not in PROFILES:
        raise ValueError("unsupported_profile")
    if profile == "synthetic":
        raise ValueError("synthetic_profile_not_permitted")
    if not isinstance(adapter_identity, str) or not adapter_identity or len(adapter_identity) > 160:
        raise ValueError("invalid_adapter_identity")
    idempotency = hashlib.sha256(
        f"divine-arsenal:v1:{input_sha256}:{profile}:{adapter_identity}".encode("ascii")
    ).hexdigest()
    job = _request("/v1/jobs", "POST", {
        "input_sha256": input_sha256, "profile": profile,
        "authority": "OBSERVE", "idempotency_key": idempotency,
    })
    safe = _safe_job(job)
    if safe.get("adapter") != adapter_identity:
        raise REAProtocolError("adapter_version_changed_during_submission")
    return safe


def _safe_job(job):
    if not isinstance(job, dict) or JOB_ID_RE.fullmatch(str(job.get("id", ""))) is None:
        raise REAProtocolError("job_schema")
    if job.get("state") not in JOB_STATES:
        raise REAProtocolError("job_state")
    safe = {"id": job["id"], "state": job["state"]}
    for key in ("input_sha256", "adapter", "profile", "authority", "error"):
        value = job.get(key)
        if isinstance(value, str):
            safe[key] = value[:200]
    for key in ("attempts", "max_attempts"):
        value = job.get(key)
        if type(value) is int and 0 <= value <= 100:
            safe[key] = value
    for key in ("created_at", "started_at", "finished_at"):
        value = job.get(key)
        if isinstance(value, (int, float)) and math.isfinite(value):
            safe[key] = value
    # Never forward token, worker_id, lease_until or internal attempt fencing data.
    return safe


def get_job(job_id):
    if not isinstance(job_id, str) or JOB_ID_RE.fullmatch(job_id) is None:
        raise ValueError("invalid_job_id")
    job = _request("/v1/jobs/" + job_id)
    return _safe_job(job)


def cancel_job(job_id):
    if not isinstance(job_id, str) or JOB_ID_RE.fullmatch(job_id) is None:
        raise ValueError("invalid_job_id")
    job = _request("/v1/jobs/" + job_id + "/cancel", "POST", {})
    return _safe_job(job)


def get_artifacts(job_id):
    if not isinstance(job_id,str) or JOB_ID_RE.fullmatch(job_id) is None:
        raise ValueError("invalid_job_id")
    result=_request("/v1/jobs/"+job_id+"/artifacts")
    if not isinstance(result,list) or len(result)>16:
        raise REAProtocolError("artifact_manifest_schema")
    seen=set()
    for item in result:
        allowed_names={"VIDEO.md","breakdown.json","report.html","report.md","storyboard.jpg","audio.png",
                       "review_tasks.json","review_answers.json","remake-jobs.json","remake-dry-run.txt","rea-video-package.zip"}
        if (not isinstance(item,dict) or set(item)!={"name","sha256","size","content_type"}
            or item.get("name") not in allowed_names or item["name"] in seen
            or not SHA256_RE.fullmatch(str(item["sha256"]))
            or type(item["size"]) is not int or not 1<=item["size"]<=MAX_ARTIFACT_BYTES
            or not isinstance(item["content_type"],str)):
            raise REAProtocolError("artifact_manifest_schema")
        seen.add(item["name"])
    return result


def get_artifact(job_id,name):
    if not isinstance(job_id,str) or JOB_ID_RE.fullmatch(job_id) is None:
        raise ValueError("invalid_job_id")
    if name not in ("VIDEO.md","breakdown.json","report.html","report.md","storyboard.jpg","audio.png",
                    "review_tasks.json","review_answers.json","remake-jobs.json","remake-dry-run.txt","rea-video-package.zip"):
        raise ValueError("invalid_artifact_name")
    base,token,timeout,_port=_settings()
    path="/v1/jobs/"+job_id+"/artifacts/"+urllib.parse.quote(name,safe="")
    request=urllib.request.Request(base+path,headers={
        "Accept":"application/octet-stream","Authorization":"Bearer "+token,
        "User-Agent":"DivineArsenal-Local-REA/1",
    })
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),_NoRedirect())
    try:
        with opener.open(request,timeout=timeout) as response:
            raw=response.read(MAX_ARTIFACT_BYTES+1)
            if len(raw)>MAX_ARTIFACT_BYTES:
                raise REAProtocolError("artifact_too_large")
            return {"data":raw,"content_type":response.headers.get("Content-Type","application/octet-stream"),
                    "filename":name}
    except urllib.error.HTTPError as error:
        if error.code==401:raise REAAuthenticationError("authentication_rejected") from error
        if error.code==403:raise REAPolicyError("authority_denied") from error
        if error.code==404:raise REANotFound("artifact_not_found") from error
        raise REAUnavailable("artifact_http_error") from error
    except REAError:
        raise
    except (urllib.error.URLError,TimeoutError,OSError,ValueError) as error:
        raise REAUnavailable("artifact_fetch_failed") from error


def get_report(job_id, job=None, adapter_descriptor=None):
    if not isinstance(job_id, str) or JOB_ID_RE.fullmatch(job_id) is None:
        raise ValueError("invalid_job_id")
    report = _request("/v1/jobs/" + job_id + "/report")
    if not isinstance(report, dict) or type(report.get("schema_version")) is not int or report["schema_version"] != 1:
        raise REAProtocolError("report_schema")
    analysis = report.get("analysis")
    if not isinstance(analysis, dict) or type(analysis.get("schema_version")) is not int or analysis["schema_version"] != 1:
        raise REAProtocolError("analysis_schema")
    inputs = analysis.get("inputs")
    evidence = analysis.get("evidence")
    findings = analysis.get("findings")
    if not isinstance(inputs, list) or not inputs or not isinstance(evidence, list) or not isinstance(findings, list):
        raise REAProtocolError("report_sections")
    input_hashes = {item.get("sha256") for item in inputs if isinstance(item, dict)}
    if not input_hashes or any(not isinstance(value, str) or SHA256_RE.fullmatch(value) is None for value in input_hashes):
        raise REAProtocolError("input_hashes")
    evidence_hashes = set()
    for item in evidence:
        if not isinstance(item, dict) or not isinstance(item.get("sha256"), str) or SHA256_RE.fullmatch(item["sha256"]) is None:
            raise REAProtocolError("evidence_schema")
        evidence_hashes.add(item["sha256"])
    safe_findings = []
    for finding in findings:
        if not isinstance(finding, dict):
            raise REAProtocolError("finding_schema")
        refs = finding.get("evidence_hashes")
        if not isinstance(refs, list) or not refs or any(ref not in evidence_hashes for ref in refs):
            raise REAProtocolError("finding_evidence_reference")
        confidence = finding.get("confidence")
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not math.isfinite(confidence) or not 0 <= confidence <= 1:
            raise REAProtocolError("finding_confidence")
        if not isinstance(finding.get("kind"), str) or not isinstance(finding.get("text"), str):
            raise REAProtocolError("finding_content")
        limitations = finding.get("limitations", [])
        if not isinstance(limitations, list) or any(not isinstance(x, str) for x in limitations):
            raise REAProtocolError("finding_limitations")
        safe_findings.append({
            "kind": finding["kind"][:40], "text": finding["text"][:4000],
            "confidence": confidence, "evidence_hashes": refs[:64],
            "source": finding.get("source", "UNKNOWN") if isinstance(finding.get("source", "UNKNOWN"), str) else "UNKNOWN",
            "limitations": [x[:500] for x in limitations[:32]],
        })
    safe_inputs = []
    for item in inputs[:8]:
        if not isinstance(item, dict) or not isinstance(item.get("sha256"), str):
            raise REAProtocolError("input_schema")
        classification = item.get("classification", {})
        if not isinstance(classification, dict):
            classification = {}
        safe_inputs.append({
            "sha256": item["sha256"], "size": item.get("size") if type(item.get("size")) is int else None,
            "classification": classification,
        })
    safe_evidence = []
    for item in evidence[:256]:
        kind = item.get("kind", "UNKNOWN")
        if not isinstance(kind, str):
            raise REAProtocolError("evidence_kind")
        safe_evidence.append({"kind": kind[:80], "sha256": item["sha256"]})
    adapters = analysis.get("adapters", [])
    if not isinstance(adapters, list) or any(not isinstance(x, str) for x in adapters):
        raise REAProtocolError("adapter_schema")
    limitations = analysis.get("limitations", [])
    if not isinstance(limitations, list) or any(not isinstance(x, str) for x in limitations):
        raise REAProtocolError("report_limitations")
    provider_limitations = [x[:500] for x in limitations[:64]]
    compatibility_notes = []
    presented_limitations = []
    legacy_limit = "Local synthetic/static analysis only; no specialized or Fleet integration"
    corrected_limit = "No runtime behaviour, device control or Fleet transport was performed; this report contains only the selected adapter's bounded local analysis."
    for limitation in provider_limitations:
        if limitation == legacy_limit:
            presented_limitations.append(corrected_limit)
            compatibility_notes.append("Normalized a legacy URE v1 generic limitation template; original provider wording is preserved in provider_limitations.")
        else:
            presented_limitations.append(limitation)
    reconstructions = analysis.get("reconstructions", [])
    if not isinstance(reconstructions, list):
        raise REAProtocolError("reconstruction_schema")
    safe_reconstructions = []
    for item in reconstructions[:64]:
        if not isinstance(item, dict):
            raise REAProtocolError("reconstruction_item")
        refs = item.get("evidence_hashes")
        sha = item.get("sha256")
        kind = item.get("kind", "UNKNOWN")
        description = item.get("text", "")
        if (not isinstance(refs, list) or not refs
                or any(ref not in evidence_hashes for ref in refs)
                or not isinstance(sha, str) or SHA256_RE.fullmatch(sha) is None
                or not isinstance(kind, str) or not isinstance(description, str)):
            raise REAProtocolError("reconstruction_evidence_reference")
        safe_reconstructions.append({
            "kind": kind[:80], "text": description[:4000],
            "sha256": sha, "evidence_hashes": refs[:64],
        })
    # Keep the execution envelope, but never expose worker IDs, attempt IDs,
    # lease timestamps, fencing tokens, raw metadata or raw stdout/stderr.
    if job is None:
        job = get_job(job_id)
    execution = report.get("execution", {})
    if not isinstance(execution, dict):
        raise REAProtocolError("execution_schema")
    attempts = execution.get("attempts", [])
    metadata = execution.get("raw_metadata", [])
    if not isinstance(attempts, list) or len(attempts) > 32 or not isinstance(metadata, list) or len(metadata) > 256:
        raise REAProtocolError("execution_records")
    starts = [a.get("started_at") for a in attempts if isinstance(a, dict)
              and isinstance(a.get("started_at"), (int, float))
              and not isinstance(a.get("started_at"), bool) and math.isfinite(a["started_at"])]
    finishes = [a.get("finished_at") for a in attempts if isinstance(a, dict)
                and isinstance(a.get("finished_at"), (int, float))
                and not isinstance(a.get("finished_at"), bool) and math.isfinite(a["finished_at"])]
    sandbox_profiles = {m.get("sandbox") for m in metadata if isinstance(m, dict)
                        and isinstance(m.get("sandbox"), str)}
    sandbox_profile = next(iter(sandbox_profiles)) if len(sandbox_profiles) == 1 else "UNKNOWN"
    exit_codes = {m.get("exit_code") for m in metadata if isinstance(m, dict) and type(m.get("exit_code")) is int}
    descriptor_limits = adapter_descriptor.get("resource_limits", {}) if isinstance(adapter_descriptor, dict) else {}
    if not isinstance(descriptor_limits, dict):
        descriptor_limits = {}
    resource_limits = {k: descriptor_limits[k] for k in ("memory_mb", "cpu_seconds", "wall_seconds", "output_bytes") if type(descriptor_limits.get(k)) is int}
    authority = job.get("authority")
    if authority != "OBSERVE":
        raise REAProtocolError("unexpected_authority")
    execution_summary = {
        "job_id": job_id,
        "input_sha256": job.get("input_sha256"),
        "adapter": job.get("adapter"),
        "profile": job.get("profile"),
        "authority": "OBSERVE",
        "permissions": ["OBSERVE"],
        "state": job.get("state"),
        "created_at": job.get("created_at"),
        "started_at": min(starts) if starts else None,
        "finished_at": max(finishes) if finishes else job.get("finished_at"),
        "attempt_count": job.get("attempts", len(attempts)),
        "sandbox_profile": sandbox_profile,
        "network_policy": "DENIED" if sandbox_profile.startswith("bubblewrap-") else "UNKNOWN",
        "filesystem_policy": "ISOLATED_READ_ONLY_INPUTS" if sandbox_profile.startswith("bubblewrap-") else "UNKNOWN",
        "exit_code": next(iter(exit_codes)) if len(exit_codes) == 1 else None,
        "timed_out": any(isinstance(m, dict) and m.get("timed_out") is True for m in metadata),
        "truncated": any(isinstance(m, dict) and m.get("truncated") is True for m in metadata),
        "cancelled": any(isinstance(m, dict) and m.get("cancelled") is True for m in metadata),
        "reaped": bool(metadata) and all(isinstance(m, dict) and m.get("reaped") is True for m in metadata),
        "error": job.get("error"),
    }
    raw_artifacts=analysis.get("artifacts",[])
    if not isinstance(raw_artifacts,list) or len(raw_artifacts)>16:
        raise REAProtocolError("artifact_manifest_schema")
    safe_artifacts=[]
    allowed_artifacts={"VIDEO.md","breakdown.json","report.html","report.md","storyboard.jpg","audio.png",
                       "review_tasks.json","review_answers.json","remake-jobs.json","remake-dry-run.txt","rea-video-package.zip"}
    seen_artifacts=set()
    for item in raw_artifacts:
        if (not isinstance(item,dict) or set(item)!={"name","sha256","size","content_type"}
            or item.get("name") not in allowed_artifacts or item["name"] in seen_artifacts
            or item.get("sha256") not in evidence_hashes or type(item.get("size")) is not int
            or not 1<=item["size"]<=MAX_ARTIFACT_BYTES or not isinstance(item.get("content_type"),str)):
            raise REAProtocolError("artifact_manifest_schema")
        seen_artifacts.add(item["name"])
        safe_artifacts.append({"name":item["name"],"sha256":item["sha256"],"size":item["size"],"content_type":item["content_type"]})
    video_summary=analysis.get("video_summary")
    if video_summary is not None:
        if (not isinstance(video_summary,dict) or type(video_summary.get("shot_count")) is not int
            or not isinstance(video_summary.get("verdict"),str)
            or not isinstance(video_summary.get("review_state"),str)):
            raise REAProtocolError("video_summary_schema")
        plan=video_summary.get("remake_plan")
        plan_keys={"status","jobs_total","generation_jobs","local_ffmpeg_jobs","keep_original_jobs",
                   "capsule_cinema_commit","paid_generation_executed"}
        if (not isinstance(plan,dict) or set(plan)!=plan_keys
            or plan.get("status") not in ("GENERATED","UNAVAILABLE")
            or any(type(plan.get(k)) is not int or not 0<=plan[k]<=10000
                   for k in ("jobs_total","generation_jobs","local_ffmpeg_jobs","keep_original_jobs"))
            or plan.get("paid_generation_executed") is not False
            or plan["jobs_total"] != plan["generation_jobs"]+plan["local_ffmpeg_jobs"]+plan["keep_original_jobs"]):
            raise REAProtocolError("video_remake_plan_schema")
        commit=plan.get("capsule_cinema_commit")
        if commit is not None and (not isinstance(commit,str) or re.fullmatch(r"[0-9a-f]{40}", commit) is None):
            raise REAProtocolError("video_remake_plan_commit")
        video_summary={k:v for k,v in video_summary.items() if k in (
            "duration_seconds","shot_count","verdict","production_mix","confidence","vlm_status",
            "review_state","transitions","overlay_kinds","real_material","remake_plan") }
    return {
        "schema_version": 1,
        "analysis": {
            "schema_version": 1, "inputs": safe_inputs,
            "adapters": adapters[:32], "evidence": safe_evidence,
            "findings": safe_findings, "reconstructions": safe_reconstructions,
            "artifacts":safe_artifacts,"video_summary":video_summary,
            "limitations": presented_limitations,
            "provider_limitations": provider_limitations,
            "compatibility_notes": compatibility_notes,
            "execution_summary": execution_summary,
            "resource_limits": resource_limits,
        },
    }
