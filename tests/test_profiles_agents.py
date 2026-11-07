import json
import tomllib
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from divine import agents, store
from divine.server import app

@pytest.fixture
def isolated(tmp_path,monkeypatch):
    monkeypatch.setenv("DIVINE_DATA_DIR",str(tmp_path/"private"))
    return tmp_path

def sample(alias, date):
    return {"alias":alias, "birth":{"date":date,"time":None,"timezone":"Australia/Sydney",
                                     "birthplace":None,"birthplace_confirmed":False},
            "current_location":{"name":"test","latitude":-33.8688,"longitude":151.2093,"timezone":"Australia/Sydney"},
            "goals":"Write and test software, research zero-star GitHub repos and produce creative videos",
            "agents":["hermes","codex","opencode"],
            "traditions":["planetary_hours"],"privacy_consent":True}

def test_profile_isolation_and_permissions(isolated):
    a=store.create_profile(sample("ALPHA","2000-10-10"))
    b=store.create_profile(sample("BETA","1995-02-01"))
    assert a["id"]!=b["id"]
    assert store.get_profile(a["id"])["birth"]["date"]=="2000-10-10"
    assert store.get_profile(b["id"])["birth"]["date"]=="1995-02-01"
    assert not any("birth" in x for x in store.list_profiles())
    assert (isolated/"private").stat().st_mode&0o777==0o700
    assert (isolated/"private"/"profiles.sqlite3").stat().st_mode&0o777==0o600

def test_private_agent_workspace_staging_and_json_toml(isolated):
    a=store.create_profile(sample("ALPHA","2000-10-10"))
    result=agents.compile_workspace(a)
    root=Path(result["path"])
    plan=json.loads((root/"plan.json").read_text())
    assert result["status"]=="staged_not_activated"
    assert {r["key"] for r in plan["roles"]}>={"engineering","research","creative"}
    assert all(not w["enabled"] for w in plan["proposed_workflows"])
    assert all(w["authority"]=="OBSERVE" for w in plan["proposed_workflows"])
    assert all(p.exists() for p in (root/"AGENTS.md",root/"opencode.json",root/".codex/config.toml"))
    tomllib.loads((root/".codex/config.toml").read_text())
    json.loads((root/"opencode.json").read_text())
    assert "2000" not in (root/"AGENTS.md").read_text()

def test_local_api_profiles_and_chart(isolated):
    client=TestClient(app)
    assert client.get("/api/health").status_code==200
    assert client.post("/api/profiles",json={**sample("NO","2000-01-01"),"privacy_consent":False}).status_code==422
    out=client.post("/api/profiles",json=sample("ALPHA","2000-10-10"))
    assert out.status_code==201,out.text
    uid=out.json()["id"]
    assert len(client.get("/api/profiles").json())==1
    natal=client.get("/api/astro/"+uid)
    assert natal.status_code==200,natal.text
    assert natal.json()["natal"]["precision"]=="date_only"
    assert len(natal.json()["planetary_clock"]["hours"])==24
    preview=client.get("/api/agents/"+uid+"/preview")
    assert preview.status_code==200
    staged=client.post("/api/agents/"+uid+"/compile",json={})
    assert staged.status_code==200,staged.text
    assert staged.json()["status"]=="staged_not_activated"
    staged_path = Path(staged.json()["path"])
    assert staged_path.is_dir()
    assert client.get("/api/kamea/Sun").json()["constant"]==111
    assert client.delete("/api/profiles/"+uid).json()["deleted"] is True
    assert not staged_path.exists()
    assert client.get("/api/profiles/"+uid).status_code==404

def test_local_api_rejects_cross_origin_write(isolated):
    client=TestClient(app)
    result=client.post("/api/profiles",json=sample("A","2000-01-01"),
                       headers={"Origin":"https://evil.example"})
    assert result.status_code==403

def test_compiler_always_disabled_by_default(isolated):
    p=store.create_profile(sample("A","2000-01-01"))
    result=agents.make_plan(p)
    assert result["authorization"]["default"]=="OBSERVE"
    assert result["authorization"]["schedulers"]=="disabled"
    assert all(not x["enabled"] for x in result["proposed_workflows"])
