"""Local command-line interface. Prints no private data unless specifically requested."""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from . import astro, server, store, agents, traditions

def main():
    p = argparse.ArgumentParser(prog="divine-universal")
    subs = p.add_subparsers(dest="command", required=True)
    subs.add_parser("serve")
    brief = subs.add_parser("today")
    brief.add_argument("--lat", type=float, required=True)
    brief.add_argument("--lon", type=float, required=True)
    brief.add_argument("--tz", required=True)
    brief.add_argument("--at", default=None)
    chart = subs.add_parser("chart")
    chart.add_argument("--dob", required=True)
    chart.add_argument("--time")
    chart.add_argument("--tz", required=True)
    square = subs.add_parser("kamea")
    square.add_argument("planet")
    subs.add_parser("profiles")
    arch = subs.add_parser("agents")
    arch.add_argument("--profile", required=True)
    arch.add_argument("--compile", action="store_true")
    args = p.parse_args()
    if args.command == "serve":
        server.main()
        return
    if args.command == "today":
        at = datetime.fromisoformat(args.at.replace("Z", "+00:00")) if args.at else datetime.now(timezone.utc)
        data = {"at_utc": at.isoformat(), "planets": astro.positions(at),
                "moon": astro.moon_state(at),
                "clock": astro.planetary_clock(at, args.lat, args.lon, args.tz)}
    elif args.command == "chart":
        data = astro.natal_chart(args.dob, args.time, args.tz)
    elif args.command == "kamea":
        data = traditions.planetary_kamea(args.planet)
    elif args.command == "profiles":
        data = store.list_profiles()
    elif args.command == "agents":
        profile = store.get_profile(args.profile)
        if not profile:
            p.error("Profile not found")
        data = agents.compile_workspace(profile) if args.compile else agents.make_plan(profile)
    else:
        p.error("Unknown command")
    print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
