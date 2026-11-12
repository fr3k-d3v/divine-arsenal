"""Loopback-only local application. No cloud account, no remote profile sharing."""
from __future__ import annotations
import json
import os
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, model_validator
from . import __version__
from . import agents, astro, store
from .research_api import router as research_router

app = FastAPI(title="Divine Arsenal Universal", version=__version__,
              docs_url=None, redoc_url=None)
app.include_router(research_router)
from .notebook_api import router as notebook_router
app.include_router(notebook_router)


class Location(BaseModel):
    name: str = Field(default="", max_length=180)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone: str = Field(min_length=1, max_length=80)

    @model_validator(mode="after")
    def valid_zone(self):
        astro.require_zone(self.timezone)
        return self


class Birth(BaseModel):
    date: date
    time: str | None = None
    timezone: str = Field(min_length=1, max_length=80)
    fold: Literal[0, 1] | None = None
    birthplace: Location | None = None
    birthplace_confirmed: bool = False

    @model_validator(mode="after")
    def valid_time(self):
        astro.require_zone(self.timezone)
        if self.time:
            astro.parse_local_birth(self.date.isoformat(), self.time, self.timezone, self.fold)
        return self


class Profile(BaseModel):
    alias: str = Field(min_length=1, max_length=64)
    birth: Birth
    current_location: Location | None = None
    goals: str = Field(default="", max_length=5000)
    agents: list[Literal["hermes", "codex", "opencode"]] = Field(default_factory=list)
    traditions: list[Literal["planetary_hours", "hermetic", "kamea", "lunar_mansions"]] = Field(
        default_factory=lambda: ["planetary_hours", "hermetic"])
    privacy_consent: bool = False

    @model_validator(mode="after")
    def consent(self):
        if not self.privacy_consent:
            raise ValueError("Explicit consent required before saving birth information locally.")
        return self


def _read_profile(profile_id: str) -> dict:
    item = store.get_profile(profile_id)
    if not item:
        raise HTTPException(404, "Profile not found")
    return item


@app.middleware("http")
async def local_security(request: Request, call_next):
    # Local-first service; no authenticated multi-user internet deployment.
    if request.client and request.client.host not in ("127.0.0.1", "::1", "testclient"):
        return JSONResponse(status_code=403, content={"detail": "Local access only"})
    host = request.headers.get("host", "")
    allowed_hosts = {"127.0.0.1", "localhost", "[::1]"}
    if request.client and request.client.host == "testclient":
        allowed_hosts.add("testserver")
    if host.split(":")[0] not in allowed_hosts and not (host.startswith("[::1]") and host[5:] in ("", ":8768")):
        return JSONResponse(status_code=400, content={"detail": "Invalid local Host"})
    origin = request.headers.get("origin")
    if (origin and origin not in ("http://127.0.0.1:8768", "http://localhost:8768")) or request.headers.get("sec-fetch-site") == "cross-site":
        return JSONResponse(status_code=403, content={"detail": "Invalid origin"})
    if request.method in ("POST", "PUT", "PATCH"):
        if request.headers.get("content-type", "").split(";")[0].strip().lower() != "application/json":
            return JSONResponse(status_code=415, content={"detail": "Use application/json"})
        # Bound chunked input too; never trust Content-Length alone.
        chunks, size = [], 0
        async for chunk in request.stream():
            size += len(chunk)
            if size > 1_048_576:
                return JSONResponse(status_code=413, content={"detail": "JSON body exceeds 1 MiB"})
            chunks.append(chunk)
        request._body = b"".join(chunks)
    response = await call_next(request)
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers.setdefault("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' blob: https://iiif.wellcomecollection.org https://tile.loc.gov https://iiif.io https://ids.lib.harvard.edu https://media.nga.gov; connect-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'none'; form-action 'self'")
    if os.environ.get("DIVINE_ALLOW_NETWORK") != "1":
        response.headers["Content-Security-Policy"] = response.headers["Content-Security-Policy"].replace("img-src 'self' blob: https://iiif.wellcomecollection.org https://tile.loc.gov https://iiif.io https://ids.lib.harvard.edu https://media.nga.gov", "img-src 'self' blob:")
    return response


@app.get("/")
def index():
    return FileResponse(Path(__file__).resolve().parent / "web" / "index.html", headers={"Cache-Control": "no-cache"})


@app.get("/api/docs", response_class=HTMLResponse, include_in_schema=False)
def api_docs():
    # Local documentation must not silently load third-party JavaScript.
    return """<!doctype html><html lang="en"><meta charset="utf-8">
    <title>Divine Arsenal local API</title><main><h1>Local API reference</h1>
    <p>Experimental, single-owner loopback API. No hosted authentication.</p>
    <p><a href="/openapi.json">OpenAPI schema with all routes and request models</a></p>
    <p><a href="/api/sources/schema">Source catalogue JSON Schema</a></p>
    <p>Source catalogue imports validate metadata only. Private notebook imports persist locally; no remote downloads.</p>
    <p><a href="/">Return to the workbench</a></p></main></html>"""


@app.get("/api/health")
def health():
    return {
        "version": __version__, "service": "divine-arsenal-universal",
        "readiness": "local_beta", "ephemeris": "astronomy-engine",
        "private_storage": str(store.private_root()),
        "global_agent_configs_changed": False,
        "active_automation": False,
        "authority": "OBSERVE",
        "local_only": os.environ.get("DIVINE_ALLOW_NETWORK") != "1",
    }


@app.get("/api/profiles")
def profiles():
    return store.list_profiles()


@app.post("/api/profiles", status_code=201)
def create_profile(input: Profile):
    return store.create_profile(input.model_dump(mode="json"))


@app.get("/api/profiles/{profile_id}")
def get_profile(profile_id: str):
    return _read_profile(profile_id)


@app.put("/api/profiles/{profile_id}")
def update_profile(profile_id: str, input: Profile):
    result = store.update_profile(profile_id, input.model_dump(mode="json"))
    if result is None:
        raise HTTPException(404, "Profile not found")
    return result


@app.delete("/api/profiles/{profile_id}")
def delete_profile(profile_id: str):
    _read_profile(profile_id)
    if not store.delete_profile(profile_id):
        raise HTTPException(404, "Profile not found")
    return {"deleted": True, "profile_id": profile_id,
            "note": "Profile database row and its staged local agent workspace removed; backups remain separate."}


@app.get("/api/astro/{profile_id}")
def get_astro(profile_id: str, at: str | None = Query(default=None, max_length=70)):
    item = _read_profile(profile_id)
    try:
        moment = datetime.fromisoformat(at.replace("Z", "+00:00")) if at else None
        return astro.briefing(item, moment)
    except (ValueError, TypeError) as exc:
        raise HTTPException(422, str(exc)) from exc


@app.get("/api/agents/capabilities")
def get_capabilities():
    return agents.installed_agents()


@app.get("/api/agents/{profile_id}/preview")
def preview_agents(profile_id: str):
    return agents.make_plan(_read_profile(profile_id))


@app.post("/api/agents/{profile_id}/compile")
def compile_agents(profile_id: str):
    # Writes solely to this profile's isolated LOCAL workspace. Never touches global agent configs.
    result = agents.compile_workspace(_read_profile(profile_id))
    return result


@app.get("/api/traditions")
def traditions():
    return {
        "systems": [
            {"id": "planetary_hours", "status": "implemented", "source": "Classical Chaldean sequence",
             "nature": "symbolic interpretation"},
            {"id": "lunar_mansions", "status": "28_equal_aries_convention", "nature": "symbolic interpretation"},
            {"id": "hermetic", "status": "minimal_correspondences", "nature": "historical symbolism"},
            {"id": "kamea", "status": "traditional_square_constants", "nature": "mathematical/artistic"},
        ],
        "limitations": ["Historical attributions and 72-name variants remain under source review",
                        "No promise of supernatural outcomes"],
    }


@app.get("/api/geo/search")
def search_location(q: str = Query(min_length=3, max_length=120)):
    """Explicit opt-in request sends searched city/place name to OpenStreetMap Nominatim."""
    if os.environ.get("DIVINE_ALLOW_NETWORK") != "1":
        raise HTTPException(403, "Local-only mode: external geocoding disabled; enter coordinates manually")
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": q, "format": "jsonv2", "limit": "5", "addressdetails": "1"})
    req = urllib.request.Request(url, headers={
        "User-Agent": "DivineArsenalUniversal/0.1 (https://github.com/fr3k-d3v/divine-arsenal)",
        "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=8) as conn:
            values = json.load(conn)
    except Exception as exc:
        raise HTTPException(503, f"Geocoding unavailable: {type(exc).__name__}") from exc
    return [{"name":x.get("display_name", ""), "latitude": float(x["lat"]),
             "longitude": float(x["lon"])} for x in values[:5]]


@app.get("/api/research")
def research():
    return {
        "zero_star_leads": [
            {"name": "ASTRON", "url": "https://github.com/retroverse-studios/astron", "note": "AGPL; study only"},
            {"name": "PlanetaryHours", "url": "https://github.com/UnitarLab/PlanetaryHours", "note": "license verify"},
            {"name": "Magickal-Time-Calculator", "url": "https://github.com/theelegantthreat/Magickal-Time-Calculator", "note": "GPL reference"},
            {"name": "Planetary Kameas", "url": "https://github.com/PoweredbyPugs/planetary-kameas", "note": "license verify"},
            {"name": "Arabic Lunar Mansions", "url": "https://github.com/ElNeMeR70/hijri-py-lunar-mansions-manazil", "note": "test required"},
        ]
    }


def main():
    import uvicorn
    uvicorn.run("divine.server:app", host="127.0.0.1", port=8768, log_level="info")


@app.get("/api/kamea/{planet}")
def get_kamea(planet: str):
    from .traditions import planetary_kamea
    try:
        return planetary_kamea(planet)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@app.get("/api/correspondence/{planet}")
def correspondence(planet: str):
    from .traditions import PLANETARY
    if planet.title() not in PLANETARY:
        raise HTTPException(404, "Unknown planet")
    return {"planet": planet.title(), "details": PLANETARY[planet.title()],
            "status": "HISTORICAL SYMBOLISM, NOT VERIFIED CAUSATION"}


if __name__ == "__main__":
    main()
