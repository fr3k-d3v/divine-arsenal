"""Testable astronomy: UTC instants, IANA time zones, precise ephemeris.

Traditional interpretations are separate and never determine machine authority.
"""
from __future__ import annotations

import math
from importlib.metadata import version
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import astronomy
from astral import Observer
from astral.sun import sun

ENGINE = {"name": "astronomy-engine", "version": version("astronomy-engine"),
          "frame": "apparent geocentric tropical ecliptic of date",
          "time_input": "UTC ISO-8601; engine derives terrestrial time internally",
          "precision_note": "Six longitude decimals are output rounding, not certified accuracy. Clock/location uncertainty remains input-dependent.",
          "validation": "Independent approximate solar vectors (Astral 3.2), 2000–2030 sample dates, 0.03 degree acceptance bound; Moon and planets await independent precision validation"}
UTC = timezone.utc
BODIES = ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn")
SIGN_NAMES = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")
CHALDEAN = ("Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon")
DAY_LORD = ("Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun")
ASPECTS = {"conjunction": (0, 8), "sextile": (60, 4), "square": (90, 6),
           "trine": (120, 6), "opposition": (180, 8)}
# Traditional dignity taxonomy, not a scientific or psychological score.
DOMICILES = {"Sun": {"Leo"}, "Moon": {"Cancer"},
             "Mercury": {"Gemini", "Virgo"}, "Venus": {"Taurus", "Libra"},
             "Mars": {"Aries", "Scorpio"}, "Jupiter": {"Sagittarius", "Pisces"},
             "Saturn": {"Capricorn", "Aquarius"}}
EXALTATIONS = {"Sun": "Aries", "Moon": "Taurus", "Mercury": "Virgo",
               "Venus": "Pisces", "Mars": "Capricorn", "Jupiter": "Cancer",
               "Saturn": "Libra"}
OPPOSITE = {SIGN_NAMES[i]: SIGN_NAMES[(i + 6) % 12] for i in range(12)}


def require_zone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError, TypeError) as exc:
        raise ValueError(f"Unknown IANA timezone: {name!r}") from exc


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Timezone-aware datetime required")
    return value.astimezone(UTC)


def parse_local_birth(date_str: str, hhmm: str, zone_name: str, fold: int | None = None) -> datetime:
    """Strictly validate ambiguous and nonexistent historical local times."""
    if fold not in (None, 0, 1):
        raise ValueError("fold must be 0 or 1")
    d = date.fromisoformat(date_str)
    t = time.fromisoformat(hhmm)
    if t.tzinfo is not None:
        raise ValueError("Birth time must be a local clock time without UTC offset")
    z = require_zone(zone_name)
    wall = datetime.combine(d, t)
    candidate = wall.replace(tzinfo=z, fold=0 if fold is None else fold)
    back = candidate.astimezone(UTC).astimezone(z).replace(tzinfo=None)
    if back != wall:
        raise ValueError("Nonexistent local birth time during daylight-saving transition")
    off0 = wall.replace(tzinfo=z, fold=0).utcoffset()
    off1 = wall.replace(tzinfo=z, fold=1).utcoffset()
    if off0 != off1 and fold is None:
        raise ValueError("Ambiguous local birth time: specify fold 0 or 1")
    if fold not in (None, 0, 1):
        raise ValueError("fold must be 0 or 1")
    return candidate.astimezone(UTC)


def _at(t: datetime) -> astronomy.Time:
    t = ensure_utc(t)
    return astronomy.Time.Make(t.year, t.month, t.day, t.hour, t.minute,
                               t.second + t.microsecond / 1_000_000)


def _angle_diff(first: float, second: float) -> float:
    return (second - first + 540) % 360 - 180


def _longitude(name: str, at: datetime) -> float:
    moment = _at(at)
    body = getattr(astronomy.Body, name)
    return float(astronomy.Ecliptic(astronomy.GeoVector(body, moment, True)).elon) % 360


def dignity(planet: str, sign: str) -> str:
    if sign in DOMICILES.get(planet, set()):
        return "domicile"
    if EXALTATIONS.get(planet) == sign:
        return "exaltation"
    if any(OPPOSITE[s] == sign for s in DOMICILES.get(planet, ())):
        return "detriment"
    if OPPOSITE.get(EXALTATIONS.get(planet)) == sign:
        return "fall"
    return "peregrine / other essential dignities not evaluated"


def positions(at: datetime) -> dict:
    at = ensure_utc(at)
    result = {}
    for planet in BODIES:
        longitude = _longitude(planet, at)
        sign = SIGN_NAMES[int(longitude // 30)]
        prev = _longitude(planet, at - timedelta(hours=12))
        nxt = _longitude(planet, at + timedelta(hours=12))
        retro = _angle_diff(prev, nxt) < 0 if planet not in ("Sun", "Moon") else False
        result[planet] = {
            "longitude": round(longitude, 6),
            "sign": sign,
            "degree_in_sign": round(longitude % 30, 4),
            "retrograde": retro,
            "dignity_traditional": dignity(planet, sign),
        }
    return result


def moon_state(at: datetime) -> dict:
    phase = float(astronomy.MoonPhase(_at(at)))
    names = ("New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
             "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent")
    index = int(((phase + 22.5) % 360) // 45)
    moon_lon = _longitude("Moon", at)
    return {
        "phase_angle_degrees": round(phase, 4),
        "phase_name": names[index],
        "approx_illumination_pct": round(100 * (1 - math.cos(math.radians(phase))) / 2, 1),
        "moon_ecliptic_longitude": round(moon_lon, 6),
        "lunar_mansion_28_equal_aries": int(moon_lon // (360 / 28)) + 1,
        "mansion_note": "One selected 28-equal-segment tropical convention; historical traditions differ",
    }


def aspects(transit: dict, natal: dict) -> list[dict]:
    found = []
    for tname, td in transit.items():
        for nname, nd in natal.items():
            separation = abs(_angle_diff(td["longitude"], nd["longitude"]))
            for kind, (angle, orb_max) in ASPECTS.items():
                orb = abs(separation - angle)
                if orb <= orb_max:
                    found.append({"transit": tname, "natal": nname, "aspect": kind,
                                  "orb_degrees": round(orb, 3)})
    return sorted(found, key=lambda a: a["orb_degrees"])


def solar_events(day: date, lat: float, lon: float, zone: str) -> tuple[datetime, datetime]:
    require_zone(zone)
    if not -90 <= lat <= 90 or not -180 <= lon <= 180:
        raise ValueError("Latitude/longitude out of range")
    try:
        result = sun(Observer(latitude=lat, longitude=lon), date=day, tzinfo=require_zone(zone))
    except ValueError as exc:
        raise ValueError("Sunrise/sunset unavailable at this location/date (polar exception)") from exc
    return ensure_utc(result["sunrise"]), ensure_utc(result["sunset"])


def planetary_hours(day: date, lat: float, lon: float, zone: str) -> list[dict]:
    """A traditional 24-hour planetary day begins at local sunrise."""
    sunrise, sunset = solar_events(day, lat, lon, zone)
    next_sunrise, _ = solar_events(day + timedelta(days=1), lat, lon, zone)
    if not sunrise < sunset < next_sunrise:
        raise ValueError("Invalid sunrise/sunset ordering")
    owner = DAY_LORD[day.weekday()]
    start_index = CHALDEAN.index(owner)
    out = []
    for i in range(24):
        if i < 12:
            begin = sunrise + (sunset - sunrise) * i / 12
            end = sunrise + (sunset - sunrise) * (i + 1) / 12
        else:
            begin = sunset + (next_sunrise - sunset) * (i - 12) / 12
            end = sunset + (next_sunrise - sunset) * (i - 11) / 12
        out.append({"number": i + 1, "ruler": CHALDEAN[(start_index + i) % 7],
                    "part": "day" if i < 12 else "night",
                    "start_utc": begin.isoformat(), "end_utc": end.isoformat(),
                    "start_local": begin.astimezone(require_zone(zone)).isoformat(),
                    "end_local": end.astimezone(require_zone(zone)).isoformat()})
    return out


def planetary_clock(at: datetime, lat: float, lon: float, zone: str) -> dict:
    at = ensure_utc(at)
    local = at.astimezone(require_zone(zone))
    today_sunrise, _ = solar_events(local.date(), lat, lon, zone)
    base = local.date() - timedelta(days=1) if at < today_sunrise else local.date()
    hours = planetary_hours(base, lat, lon, zone)
    current = next((h for h in hours if datetime.fromisoformat(h["start_utc"]) <= at
                    < datetime.fromisoformat(h["end_utc"])), None)
    return {"solar_date": base.isoformat(), "local_zone": zone,
            "current": current, "hours": hours,
            "rule": "Traditional Chaldean planetary-hour sequence (interpretive)"}


def natal_chart(birth_date: str, birth_time: str | None, birth_zone: str,
                fold: int | None = None) -> dict:
    date.fromisoformat(birth_date)
    if birth_time:
        at = parse_local_birth(birth_date, birth_time, birth_zone, fold)
        return {"label": "CALCULATION", "engine": ENGINE,
                "precision": "exact_recorded_clock_time", "birth_utc": at.isoformat(),
                "positions": positions(at), "houses": None, "ascendant": None,
                "limitations": ["House and Ascendant calculations not yet implemented."]}

    z = require_zone(birth_zone)
    d = date.fromisoformat(birth_date)
    samples = [
        datetime.combine(d, time(0, 0), z).astimezone(UTC),
        datetime.combine(d, time(12, 0), z).astimezone(UTC),
        datetime.combine(d, time(23, 59), z).astimezone(UTC),
    ]
    p0, p1, p2 = [positions(t) for t in samples]
    midpoint = {}
    for planet in BODIES:
        possible_signs = sorted({p0[planet]["sign"], p1[planet]["sign"], p2[planet]["sign"]})
        midpoint[planet] = {**p1[planet], "possible_signs": possible_signs,
                            "approximate": True}
    return {"label": "CALCULATION", "engine": ENGINE,
            "precision": "date_only", "sample_label": "illustrative local-noon positions",
            "positions": midpoint, "houses": None, "ascendant": None,
            "limitations": ["Birth time missing: positions are noon samples, not a natal instant.",
                            "No ascendant, houses, angular lots or precise natal aspects.",
                            "Different local clock times on this date may give different signs."]}


def briefing(profile: dict, at: datetime | None = None) -> dict:
    now = ensure_utc(at or datetime.now(UTC))
    birth = profile["birth"]
    natal = natal_chart(birth["date"], birth.get("time"), birth["timezone"], birth.get("fold"))
    locale = profile.get("current_location") or {}
    lat = locale.get("latitude")
    lon = locale.get("longitude")
    zone = locale.get("timezone")
    clock = None
    if lat is not None and lon is not None and zone:
        try:
            clock = planetary_clock(now, lat, lon, zone)
        except ValueError as exc:
            clock = {"error": str(exc)}
    current_pos = positions(now)
    return {
        "engine": ENGINE, "label": "CALCULATION",
        "at_utc": now.isoformat(), "astro_engine": "cosinekitty/astronomy-engine",
        "reference_frame": "apparent geocentric tropical ecliptic-of-date",
        "natal": natal, "transit": current_pos, "moon": moon_state(now),
        "planetary_clock": clock,
        "transit_to_natal": aspects(current_pos, natal["positions"]) if birth.get("time") else [],
        "labels": {"astronomy": "CALCULATION",
                   "traditional_dignity": "HISTORICAL INTERPRETATION",
                   "planetary_hour_meaning": "USER-SELECTED SYMBOLISM",
                   "prediction": "NOT SCIENTIFICALLY VALIDATED"},
    }
