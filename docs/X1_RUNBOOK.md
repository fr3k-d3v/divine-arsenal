# X1 local operator runbook

Installed project path on X1: `~/FR3K/divine-arsenal-universal`.
Private runtime data: `~/.local/share/divine-arsenal`.
Service: `systemctl --user status divine-arsenal-universal.service`.
Browse **on X1 itself**: http://127.0.0.1:8768/

```bash
cd ~/FR3K/divine-arsenal-universal
uv sync --extra test
uv run pytest -q
systemctl --user status divine-arsenal-universal.service
curl -fsS http://127.0.0.1:8768/api/health
journalctl --user -u divine-arsenal-universal.service -n 50 --no-pager
```

For a private user profile, use the browser onboarding. Do not commit private data.
The profile form asks date of birth, optional time, city/coordinates, IANA timezone,
declared goals, desired agents and consent. Review stored fields before use.
The `DEMO SYNTHETIC` test profile is not a real person's profile.

After building a personal plan, the Agent Architect stages project-scoped files under
`~/.local/share/divine-arsenal/workspaces/<profile UUID>/`. Open that directory with
Codex or OpenCode if you trust it. For Hermes review the staged SKILL.md and install
separately only after authorization; the active original skill is never replaced.
No agent actions, schedulers, cloud model calls, deployments or fleet commands run
merely because a plan was generated.

The service binds only to loopback. Do **not** reverse proxy or port-forward
this beta to the public internet; it lacks hosted-account authentication.

Diagnosis: a running PID alone is not success. Verify HTTP 200, state content,
specific chart output and actual front-end interactions.
