from fastapi.testclient import TestClient
from divine.server import app


def test_master_hero_is_served_from_local_assets():
    response = TestClient(app).get("/assets/divine-arsenal-master-hero.webp")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/webp")
    assert len(response.content) > 10_000
