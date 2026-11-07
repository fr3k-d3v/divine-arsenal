"""Read-only MCP computation tools; never expose private saved profiles or grant writes."""
from __future__ import annotations
from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP
from . import astro, traditions

mcp = FastMCP("divine-arsenal-universal")

@mcp.tool()
def planet_positions(at_utc: str) -> dict:
    """Compute apparent geocentric tropical planetary positions from explicit UTC ISO timestamp."""
    at = datetime.fromisoformat(at_utc.replace("Z", "+00:00"))
    return {"positions": astro.positions(at),
            "reference_frame": "geocentric tropical true ecliptic of date",
            "ephemeris": "astronomy-engine", "label": "CALCULATION"}

@mcp.tool()
def natal_positions(birth_date: str, birth_zone: str, birth_time: str = "") -> dict:
    """Compute from data supplied explicitly in this tool call; no saved-profile access."""
    return astro.natal_chart(birth_date, birth_time or None, birth_zone)

@mcp.tool()
def planetary_hours(at_utc: str, latitude: float, longitude: float, timezone_name: str) -> dict:
    """Traditional 24 unequal planetary hours for a location and a UTC instant."""
    at = datetime.fromisoformat(at_utc.replace("Z", "+00:00"))
    return astro.planetary_clock(at, latitude, longitude, timezone_name)

@mcp.tool()
def kamea(planet: str) -> dict:
    """Generate a mathematically validated planetary magic square for symbolic study."""
    return traditions.planetary_kamea(planet)

@mcp.tool()
def planetary_correspondence(planet: str) -> dict:
    """Traditional symbolism, never empirical predictions or agent permissions."""
    if planet not in traditions.PLANETARY:
        raise ValueError("Unknown traditional planet")
    return {"planet": planet, "source_family": "Arbatel and conventional correspondences",
            "interpretation": traditions.PLANETARY[planet],
            "status": "HISTORICAL / INTERPRETIVE"}

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
