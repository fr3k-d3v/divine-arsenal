from datetime import date, datetime, timedelta, timezone
import pytest
from divine import astro

UTC = timezone.utc

def test_precise_longitudes_and_solar_equinox():
    pos = astro.positions(datetime(2026, 3, 20, 15, 46, tzinfo=UTC))
    assert pos["Sun"]["sign"] in ("Pisces", "Aries")
    assert pos["Sun"]["degree_in_sign"] > 28 or pos["Sun"]["degree_in_sign"] < 2
    for p in astro.BODIES:
        assert 0 <= pos[p]["longitude"] < 360
        assert 0 <= pos[p]["degree_in_sign"] < 30

def test_2000_solar_position_is_near_libra_17_not_hardcoded():
    p = astro.positions(datetime(2000, 10, 10, 2, 0, tzinfo=UTC))
    assert p["Sun"]["sign"] == "Libra"
    assert 15 <= p["Sun"]["degree_in_sign"] <= 19

def test_24_continuous_solar_hours_and_lords():
    for d, ruler in [(date(2026,11,7), "Saturn"),
                     (date(2026,11,8), "Sun"),
                     (date(2026,11,9), "Moon")]:
        hours = astro.planetary_hours(d, -33.8688, 151.2093, "Australia/Sydney")
        assert len(hours) == 24
        assert hours[0]["ruler"] == ruler
        assert all(datetime.fromisoformat(h["end_utc"]) > datetime.fromisoformat(h["start_utc"]) for h in hours)
        for a,b in zip(hours,hours[1:]):
            assert datetime.fromisoformat(a["end_utc"]) == datetime.fromisoformat(b["start_utc"])

def test_clock_after_midnight_uses_previous_sunrise():
    now = datetime(2026,11,7,2,0,tzinfo=UTC)
    clock = astro.planetary_clock(now,-33.8688,151.2093,"Australia/Sydney")
    assert len(clock["hours"]) == 24
    assert clock["current"] is not None

def test_dst_historical_transition_is_utc_consecutive():
    hours=astro.planetary_hours(date(2026,3,8),40.7128,-74.006,"America/New_York")
    assert len(hours)==24
    for a,b in zip(hours,hours[1:]):
        assert a["end_utc"]==b["start_utc"]

def test_ambiguous_and_nonexistent_birth_clock():
    with pytest.raises(ValueError,match="Ambiguous"):
        astro.parse_local_birth("2026-11-01","01:30","America/New_York")
    t0=astro.parse_local_birth("2026-11-01","01:30","America/New_York",0)
    t1=astro.parse_local_birth("2026-11-01","01:30","America/New_York",1)
    assert t1-t0==timedelta(hours=1)
    with pytest.raises(ValueError,match="Nonexistent"):
        astro.parse_local_birth("2026-03-08","02:30","America/New_York")

def test_birth_date_only_rejects_false_houses():
    natal=astro.natal_chart("2000-10-10",None,"Australia/Sydney")
    assert natal["precision"]=="date_only"
    assert natal["houses"] is None and natal["ascendant"] is None
    assert natal["positions"]["Moon"]["approximate"]

def test_traditional_dignity_corrections():
    assert astro.dignity("Moon","Taurus")=="exaltation"
    assert astro.dignity("Moon","Pisces")!="exaltation"
    assert astro.dignity("Sun","Libra")=="fall"
    assert astro.dignity("Jupiter","Libra")!="detriment"

def test_no_timezone_naive_fake_precision():
    with pytest.raises(ValueError):
        astro.positions(datetime(2026,11,7))
    with pytest.raises(ValueError):
        astro.natal_chart("2026-01-01","12:00","Invalid/Zone")


def test_independent_approximate_solar_vectors():
    """Cross-engine regression, not an observational accuracy certificate."""
    import json
    from pathlib import Path
    from astral.sun import sun_apparent_long
    from astral.julian import julianday, julianday_to_juliancentury
    from divine import astro
    fixture = json.loads(Path('tests/fixtures/solar-independent.json').read_text())
    assert fixture['label'] == 'CALCULATION'
    for vector in fixture['vectors']:
        at = datetime.fromisoformat(vector['utc'])
        independently_computed = sun_apparent_long(julianday_to_juliancentury(julianday(at))) % 360
        assert abs(astro._angle_diff(independently_computed, vector['sun_longitude_degrees'])) < 1e-7
        calculated = astro.positions(at)['Sun']['longitude']
        assert abs(astro._angle_diff(calculated, vector['sun_longitude_degrees'])) < fixture['tolerance_degrees']
