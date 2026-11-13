#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
DIVINE_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
URE_ROOT="$HOME/FR3K/fr3k-reverse-engineering"
ENV_FILE="$HOME/.config/fr3k/divine-arsenal.env"
UNIT_DIR="$HOME/.config/systemd/user"

if [[ ! -x "$DIVINE_ROOT/.venv/bin/divine-universal" ]]; then
  echo "Missing Divine Arsenal virtual environment: $DIVINE_ROOT/.venv" >&2
  exit 1
fi
if [[ ! -x "$URE_ROOT/.venv/bin/python" ]]; then
  echo "Missing URE virtual environment: $URE_ROOT/.venv" >&2
  exit 1
fi
if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing private REA environment file: $ENV_FILE" >&2
  exit 1
fi

mkdir -p "$HOME/.config/fr3k" "$UNIT_DIR"
chmod 700 "$HOME/.config/fr3k"
chmod 600 "$ENV_FILE"

python3 - "$ENV_FILE" <<'PYCONFIG'
from pathlib import Path
import sys
values = {}
for line in Path(sys.argv[1]).read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    key, value = line.split("=", 1)
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        value = value[1:-1]
    values[key] = value
assert values.get("URE_URL") == "http://127.0.0.1:18879", "URE_URL must be numeric loopback"
assert len(values.get("URE_API_TOKEN", "").encode()) >= 32, "URE_API_TOKEN must be at least 32 bytes"
PYCONFIG

python3 - "$SCRIPT_DIR/../deploy/systemd" "$UNIT_DIR" "$URE_ROOT" "$DIVINE_ROOT" "$ENV_FILE" <<'PYUNITS'
from pathlib import Path
import sys
source, target, ure_root, divine_root, env_file = map(Path, sys.argv[1:])
for name in ("fr3k-ure.service", "divine-arsenal.service"):
    body = (source / name).read_text()
    body = body.replace("@URE_ROOT@", str(ure_root))
    body = body.replace("@DIVINE_ROOT@", str(divine_root))
    body = body.replace("@ENV_FILE@", str(env_file))
    output = target / name
    output.write_text(body)
    output.chmod(0o600)
PYUNITS

systemctl --user daemon-reload
systemctl --user enable --now fr3k-ure.service
systemctl --user restart fr3k-ure.service
systemctl --user enable --now divine-arsenal.service
systemctl --user restart divine-arsenal.service

for attempt in $(seq 1 100); do
  if curl -fsS --max-time 1 http://127.0.0.1:18879/v1/health >/dev/null 2>&1 &&
     curl -fsS --max-time 1 http://127.0.0.1:8768/api/rea/status 2>/dev/null | grep -q '"status":"READY'; then
    break
  fi
  sleep 0.2
done

systemctl --user is-active --quiet fr3k-ure.service
systemctl --user is-active --quiet divine-arsenal.service
curl -fsS --max-time 4 http://127.0.0.1:8768/api/rea/status |
  python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["status"] == "READY"; print("REA READY; adapter identities:", len(d["adapters"]))'
echo "Enabled and started fr3k-ure.service and divine-arsenal.service."
