import base64
import hashlib
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
from fastapi.testclient import TestClient

from divine.server import app


class FakeURE:
    def __init__(self):
        self.state = {
            "input": None,
            "job": {
                "id": "a" * 32, "input_sha256": "", "adapter": "identify@1.0.0",
                "profile": "identify", "authority": "OBSERVE", "state": "succeeded",
                "attempts": 1, "max_attempts": 2, "created_at": 1.0,
                "finished_at": 2.0, "token": "must-not-leak", "worker_id": "private-worker",
                "lease_until": 9999999999,
            },
            "job_request": None,
            "bad_report": False,
            "report_input_sha": None,
            "ghidra_version": "1.0.0",
        }
        self.evidence_sha = hashlib.sha256(b"raw classification evidence").hexdigest()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), self.handler())
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def handler(self):
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def send_json(self, status, payload):
                raw = json.dumps(payload, separators=(",", ":")).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            def read_json(self):
                return json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))))

            def do_GET(self):
                if self.path == "/v1/health":
                    return self.send_json(200, {"status": "ok", "schema_version": 1})
                if self.path == "/v1/adapters":
                    items = []
                    for identity, name in (
                        ("identify@1.0.0", "identify"),
                        ("elf.metadata@1.0.0", "elf"),
                        ("ghidra.decompile@1.0.0", "ghidra"),
                        ("jadx.decompile@1.0.0", "jadx"),
                        ("radare2.analyze@1.0.0", "radare2"),
                        ("binwalk.scan@1.0.0", "binwalk"),
                        ("unblob.scan@1.0.0", "unblob"),
                        ("kaitai.dex@1.0.0", "kaitai"),
                        ("pdf.metadata@1.0.0", "pdf.metadata"),
                        ("tei.validate@1.0.0", "tei.validate"),
                        ("iiif.manifest@1.0.0", "iiif.manifest"),
                        ("image.metadata@1.0.0", "image.metadata"),
                        ("grid.inspect@1.0.0", "grid.inspect"),
                    ):
                        if name == "ghidra":
                            identity = "ghidra.decompile@" + owner.state["ghidra_version"]
                        items.append({
                            "identity": identity, "name": name, "version": identity.rsplit("@", 1)[-1],
                            "status": "SUPPORTED", "required_authority": "OBSERVE",
                            "formats": ["*"], "capabilities": ["static-analysis"],
                            "limitations": ["Local synthetic/static analysis only; no specialized or Fleet integration"], "available": True,
                            "installed": True, "verified": identity != "elf.metadata@1.0.0", "enabled": True,
                        })
                    return self.send_json(200, items)
                if self.path == "/v1/workers":
                    return self.send_json(200, {"capabilities": {
                        "architecture": "x86_64", "memory_mb": 8192, "cpu": 8,
                        "authority": "OBSERVE",
                    }, "sandbox": {"isolation_verified": True}})
                if self.path == "/v1/jobs/" + "a" * 32:
                    return self.send_json(200, owner.state["job"])
                if self.path == "/v1/jobs/" + "a" * 32 + "/report":
                    sha = owner.state["report_input_sha"] or owner.state["job"]["input_sha256"]
                    evidence_sha = owner.evidence_sha
                    if owner.state["bad_report"]:
                        evidence_sha = "0" * 64
                    report = {
                        "schema_version": 1,
                        "analysis": {
                            "schema_version": 1,
                            "inputs": [{
                                "sha256": sha, "size": 13,
                                "classification": {"format": "elf", "confidence": 0.95},
                            }],
                            "adapters": ["identify@1.0.0"],
                            "evidence": [{"kind": "stdout", "sha256": owner.evidence_sha}],
                            "findings": [{
                                "kind": "OBSERVATION", "text": "ELF signature observed",
                                "confidence": 1.0, "evidence_hashes": [evidence_sha],
                                "source": "identify", "limitations": ["signature only"],
                            }],
                            "reconstructions": [],
                            "limitations": ["Local synthetic/static analysis only; no specialized or Fleet integration"],
                        },
                        "execution": {"attempts": [{"token": "must-not-leak"}]},
                    }
                    return self.send_json(200, report)
                return self.send_json(404, {"error": "not_found"})

            def do_POST(self):
                data = self.read_json()
                if self.path == "/v1/inputs":
                    raw = base64.b64decode(data["content_base64"], validate=True)
                    sha = hashlib.sha256(raw).hexdigest()
                    owner.state["input"] = raw
                    owner.state["job"]["input_sha256"] = sha
                    filename = data["filename"].lower()
                    suffix = filename.rsplit(".", 1)[-1] if "." in filename else ""
                    if raw.startswith(b"%PDF-"):
                        fmt, mime = "pdf", "application/pdf"
                    elif b"tei-c.org/ns/1.0" in raw and suffix in ("xml", "tei"):
                        fmt, mime = "tei_xml", "application/tei+xml"
                    elif b"presentation/3" in raw and b"Manifest" in raw and suffix == "json":
                        fmt, mime = "iiif_manifest", "application/ld+json"
                    elif raw.startswith(b"\x89PNG\r\n\x1a\n"):
                        fmt, mime = "image.png", "image/png"
                    elif raw.startswith(b"\xff\xd8\xff"):
                        fmt, mime = "image.jpeg", "image/jpeg"
                    elif raw.startswith((b"II*\x00", b"MM\x00*", b"II+\x00", b"MM\x00+")):
                        fmt, mime = "image.tiff", "image/tiff"
                    elif suffix == "csv":
                        fmt, mime = "grid.csv", "text/csv"
                    elif suffix == "tsv":
                        fmt, mime = "grid.tsv", "text/tab-separated-values"
                    else:
                        fmt, mime = "elf", "application/x-elf"
                    return self.send_json(201, {
                        "sha256": sha, "size": len(raw), "original_name": data["filename"],
                        "classification": {
                            "format": fmt, "mime": mime,
                            "architecture": "unknown", "confidence": 0.95,
                            "reasons": ["Fake test classifier: fixture signature/extension"], "limitations": ["test only"],
                        },
                    })
                if self.path == "/v1/jobs":
                    owner.state["job_request"] = data
                    adapter_for_profile = {
                        "identify": "identify@1.0.0", "elf": "elf.metadata@1.0.0",
                        "ghidra": "ghidra.decompile@" + owner.state["ghidra_version"],
                        "jadx": "jadx.decompile@1.0.0", "binwalk": "binwalk.scan@1.0.0",
                        "radare2": "radare2.analyze@1.0.0", "unblob": "unblob.scan@1.0.0",
                        "kaitai": "kaitai.dex@1.0.0", "pdf": "pdf.metadata@1.0.0",
                        "tei": "tei.validate@1.0.0", "iiif": "iiif.manifest@1.0.0",
                        "image": "image.metadata@1.0.0", "grid": "grid.inspect@1.0.0",
                    }
                    owner.state["job"].update(
                        input_sha256=data["input_sha256"], profile=data["profile"],
                        adapter=adapter_for_profile[data["profile"]],
                        authority=data["authority"], state="queued",
                    )
                    return self.send_json(202, owner.state["job"])
                if self.path == "/v1/jobs/" + "a" * 32 + "/cancel":
                    owner.state["job"]["state"] = "cancelled"
                    return self.send_json(200, owner.state["job"])
                return self.send_json(404, {"error": "not_found"})

        return Handler

    @property
    def url(self):
        return f"http://127.0.0.1:{self.server.server_address[1]}"

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(3)


@pytest.fixture
def fake_ure(monkeypatch):
    fake = FakeURE()
    monkeypatch.setenv("URE_URL", fake.url)
    monkeypatch.setenv("URE_API_TOKEN", "t" * 48)
    monkeypatch.setenv("URE_TIMEOUT", "5")
    yield fake
    fake.close()


def test_rea_status_is_local_and_does_not_expose_token(fake_ure):
    with TestClient(app) as client:
        result = client.get("/api/rea/status")
    assert result.status_code == 200
    data = result.json()
    assert data["status"] == "READY"
    assert data["endpoint"].startswith("127.0.0.1:")
    assert data["worker"]["architecture"] == "x86_64"
    assert all("token" not in key.lower() for key in data)
    assert "t" * 48 not in json.dumps(data)


def test_upload_hashes_and_recommends_only_verified_available_profiles(fake_ure):
    raw = b"\x7fELF" + b"owned test"
    payload = {"filename": "owned.elf", "content_base64": base64.b64encode(raw).decode()}
    with TestClient(app) as client:
        result = client.post("/api/rea/inputs", json=payload)
    assert result.status_code == 201, result.text
    data = result.json()
    assert data["input"]["sha256"] == hashlib.sha256(raw).hexdigest()
    assert data["input"]["size"] == len(raw)
    assert [x["profile"] for x in data["suggested_profiles"]] == [
        "identify", "ghidra", "radare2", "binwalk", "unblob"
    ]
    assert all(x["authority"] == "OBSERVE" for x in data["suggested_profiles"])
    assert fake_ure.state["input"] == raw


def test_job_creation_is_observe_only_and_hides_fencing_fields(fake_ure):
    sha = hashlib.sha256(b"owned").hexdigest()
    with TestClient(app) as client:
        result = client.post("/api/rea/jobs", json={"input_sha256": sha, "profile": "ghidra"})
    assert result.status_code == 202, result.text
    data = result.json()
    assert data["state"] == "queued"
    assert data["authority"] == "OBSERVE"
    assert fake_ure.state["job_request"]["authority"] == "OBSERVE"
    assert "token" not in data and "worker_id" not in data and "lease_until" not in data


def test_adapter_version_is_resolved_from_live_registry_and_in_idempotency_key(fake_ure):
    sha = hashlib.sha256(b"same artifact").hexdigest()
    with TestClient(app) as client:
        first = client.post("/api/rea/jobs", json={"input_sha256": sha, "profile": "ghidra"})
        assert first.status_code == 202, first.text
        first_key = fake_ure.state["job_request"]["idempotency_key"]
        assert first.json()["adapter"] == "ghidra.decompile@1.0.0"
        fake_ure.state["ghidra_version"] = "2.0.0"
        second = client.post("/api/rea/jobs", json={"input_sha256": sha, "profile": "ghidra"})
        assert second.status_code == 202, second.text
        second_key = fake_ure.state["job_request"]["idempotency_key"]
        assert second.json()["adapter"] == "ghidra.decompile@2.0.0"
    assert first_key != second_key


def test_synthetic_auto_profile_is_not_exposed(fake_ure):
    with TestClient(app) as client:
        result = client.post("/api/rea/jobs", json={
            "input_sha256": "a" * 64, "profile": "synthetic", "authority": "AUTO"
        })
    assert result.status_code == 422


def test_report_checks_input_and_evidence_links_and_strips_execution(fake_ure):
    sha = hashlib.sha256(b"owned").hexdigest()
    fake_ure.state["job"]["input_sha256"] = sha
    with TestClient(app) as client:
        result = client.get("/api/rea/jobs/" + "a" * 32 + "/report")
    assert result.status_code == 200, result.text
    data = result.json()
    assert data["analysis"]["inputs"][0]["sha256"] == sha
    assert data["analysis"]["findings"][0]["kind"] == "OBSERVATION"
    assert "execution" not in data
    assert "must-not-leak" not in json.dumps(data)
    assert data["analysis"]["provider_limitations"] == ["Local synthetic/static analysis only; no specialized or Fleet integration"]
    assert "no specialized" not in data["analysis"]["limitations"][0].lower()
    assert data["analysis"]["compatibility_notes"]


def test_report_rejects_dangling_evidence_reference(fake_ure):
    sha = hashlib.sha256(b"owned").hexdigest()
    fake_ure.state["job"]["input_sha256"] = sha
    fake_ure.state["bad_report"] = True
    with TestClient(app) as client:
        result = client.get("/api/rea/jobs/" + "a" * 32 + "/report")
    assert result.status_code == 502


def test_cancel_job_returns_safe_terminal_state(fake_ure):
    with TestClient(app) as client:
        result = client.post("/api/rea/jobs/" + "a" * 32 + "/cancel", json={})
    assert result.status_code == 200
    assert result.json()["state"] == "cancelled"
    assert "token" not in result.json()


def test_rea_not_configured_is_explicit(monkeypatch):
    monkeypatch.delenv("URE_API_TOKEN", raising=False)
    with TestClient(app) as client:
        result = client.get("/api/rea/status")
    assert result.status_code == 200
    assert result.json()["status"] == "NOT_CONFIGURED"
    assert result.json()["adapters"] == []


def test_rea_rejects_non_loopback_url(monkeypatch):
    monkeypatch.setenv("URE_URL", "http://192.0.2.10:18879")
    monkeypatch.setenv("URE_API_TOKEN", "t" * 48)
    with TestClient(app) as client:
        status = client.get("/api/rea/status")
        upload = client.post("/api/rea/inputs", json={
            "filename": "owned.bin", "content_base64": base64.b64encode(b"owned").decode()
        })
    assert status.json()["status"] == "NOT_CONFIGURED"
    assert upload.status_code == 503


def test_upload_rejects_path_components_and_oversize(fake_ure):
    with TestClient(app) as client:
        bad_name = client.post("/api/rea/inputs", json={
            "filename": "../owned.bin", "content_base64": base64.b64encode(b"owned").decode()
        })
        too_large = client.post("/api/rea/inputs", json={
            "filename": "large.bin", "content_base64": base64.b64encode(b"x" * 700_001).decode()
        })
    assert bad_name.status_code == 422
    assert too_large.status_code == 413


def test_job_report_input_must_match_job(fake_ure):
    fake_ure.state["job"]["input_sha256"] = hashlib.sha256(b"different").hexdigest()
    fake_ure.state["report_input_sha"] = hashlib.sha256(b"report-input").hexdigest()
    with TestClient(app) as client:
        result = client.get("/api/rea/jobs/" + "a" * 32 + "/report")
    assert result.status_code == 502


def test_notebook_reference_deduplicates_repeated_evidence_hashes(monkeypatch):
    from divine import rea_api

    input_sha = hashlib.sha256(b"notebook input").hexdigest()
    evidence_sha = hashlib.sha256(b"identical empty stream").hexdigest()
    job = {
        "id": "a" * 32, "input_sha256": input_sha,
        "adapter": "identify@1.0.0", "profile": "identify",
        "authority": "OBSERVE", "state": "succeeded",
    }
    report = {"analysis": {
        "execution_summary": {
            "authority": "OBSERVE", "created_at": 1.0,
            "started_at": 2.0, "finished_at": 3.0,
            "attempt_count": 1, "sandbox_profile": "test-static-v1",
            "network_policy": "UNKNOWN", "filesystem_policy": "UNKNOWN",
            "permissions": ["OBSERVE"], "exit_code": 0,
            "timed_out": False, "truncated": False,
            "cancelled": False, "reaped": True, "error": None,
        },
        "resource_limits": {
            "cpu_seconds": 2, "memory_mb": 512,
            "wall_seconds": 5, "output_bytes": 1024,
        },
        "evidence": [
            {"kind": "stdout", "sha256": evidence_sha},
            {"kind": "stderr", "sha256": evidence_sha},
        ],
        "findings": [{
            "kind": "OBSERVATION", "text": "Static signature observed",
            "confidence": 1.0, "evidence_hashes": [evidence_sha],
            "source": "identify", "limitations": [],
        }],
        "reconstructions": [], "limitations": [],
        "provider_limitations": [], "compatibility_notes": [],
    }}
    captured = {}
    monkeypatch.setattr(rea_api, "_job_report", lambda _job_id: (job, report))
    monkeypatch.setattr(rea_api.notebook, "listing", lambda _kind: [])
    def capture_save(request):
        captured["document"] = request.document
        return {"id": "c" * 32, "revision": 1}
    monkeypatch.setattr(rea_api.notebook, "save", capture_save)

    with TestClient(app) as client:
        result = client.post("/api/rea/jobs/" + job["id"] + "/notebook", json={
            "title": "Repeated evidence hashes", "note": "Regression test",
        })

    assert result.status_code == 201, result.text
    assert captured["document"].evidence_hashes == [evidence_sha]


def test_scholarly_profiles_are_suggested_and_submittable(fake_ure):
    cases = [
        ("sample.pdf", b"%PDF-1.7", "pdf", "pdf", "pdf.metadata@1.0.0"),
        ("sample.tei.xml", b'<TEI xmlns="http://www.tei-c.org/ns/1.0"/>', "tei_xml", "tei", "tei.validate@1.0.0"),
        ("sample.iiif.json", b'{"@context":"http://iiif.io/api/presentation/3/context.json","type":"Manifest"}', "iiif_manifest", "iiif", "iiif.manifest@1.0.0"),
        ("sample.png", b"\x89PNG\r\n\x1a\n", "image.png", "image", "image.metadata@1.0.0"),
        ("sample.jpg", b"\xff\xd8\xff", "image.jpeg", "image", "image.metadata@1.0.0"),
        ("sample.tiff", b"II*\x00", "image.tiff", "image", "image.metadata@1.0.0"),
        ("sample.csv", b"Name,Value\n", "grid.csv", "grid", "grid.inspect@1.0.0"),
        ("sample.tsv", b"Name\tValue\n", "grid.tsv", "grid", "grid.inspect@1.0.0"),
    ]
    with TestClient(app) as client:
        for filename, raw, expected_format, profile, expected_adapter in cases:
            upload = client.post("/api/rea/inputs", json={
                "filename": filename,
                "content_base64": base64.b64encode(raw).decode(),
            })
            assert upload.status_code == 201, (filename, upload.text)
            data = upload.json()
            assert data["input"]["classification"]["format"] == expected_format
            suggestions = [item["profile"] for item in data["suggested_profiles"]]
            assert profile in suggestions, (filename, suggestions)
            job = client.post("/api/rea/jobs", json={
                "input_sha256": hashlib.sha256(raw).hexdigest(),
                "profile": profile,
            })
            assert job.status_code == 202, (filename, job.text)
            assert job.json()["adapter"] == expected_adapter
            assert job.json()["authority"] == "OBSERVE"
    assert fake_ure.state["job_request"]["profile"] == "grid"
