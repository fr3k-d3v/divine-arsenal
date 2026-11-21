"""Regression: Git commit identifiers are not SHA-256 evidence hashes."""
import pytest
from divine import rea_client


@pytest.mark.parametrize("commit", ["97229260c96ee8a3fb37db83027bbc1aefd8f073", None])
def test_video_report_accepts_git_commit(monkeypatch, commit):
    report = _report(commit)
    monkeypatch.setattr(rea_client, "_request", lambda *args, **kwargs: report)
    result = rea_client.get_report("a" * 32, job={"authority": "OBSERVE"})
    assert result["analysis"]["video_summary"]["remake_plan"]["capsule_cinema_commit"] == commit


@pytest.mark.parametrize("commit", ["a" * 64, "g" * 40, "a" * 39, 123, "A" * 40])
def test_video_report_rejects_malformed_git_commit(monkeypatch, commit):
    monkeypatch.setattr(rea_client, "_request", lambda *args, **kwargs: _report(commit))
    with pytest.raises(rea_client.REAProtocolError, match="video_remake_plan_commit"):
        rea_client.get_report("a" * 32, job={"authority": "OBSERVE"})


def _report(commit):
    return {"schema_version": 1, "analysis": {
        "schema_version": 1, "inputs": [{"sha256": "b" * 64}],
        "evidence": [], "findings": [],
        "video_summary": {"shot_count": 1, "verdict": "tool observation", "review_state": "PENDING",
            "remake_plan": {"status": "GENERATED", "jobs_total": 0,
                "generation_jobs": 0, "local_ffmpeg_jobs": 0, "keep_original_jobs": 0,
                "capsule_cinema_commit": commit, "paid_generation_executed": False}}}}
