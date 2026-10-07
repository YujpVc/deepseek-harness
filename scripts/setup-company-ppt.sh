#!/usr/bin/env bash
set -euo pipefail

# Deploy the PPT profile with the currently selected cc-switch Codex account.
# The API key is copied only to the DSH credential file (mode 600); it is never
# printed, committed, or placed in a repository configuration file.

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
DSH_HOME_DIR="${DSH_HOME:-$HOME/.dsh}"
CC_SWITCH_DB="${CC_SWITCH_DB:-$HOME/.cc-switch/cc-switch.db}"
PROVIDER_NAME='公司_个人'

if [[ ! -f "$CC_SWITCH_DB" ]]; then
  echo "cc-switch database not found: $CC_SWITCH_DB" >&2
  exit 1
fi

mkdir -p "$DSH_HOME_DIR/profiles/web" "$DSH_HOME_DIR/.agent-presets"

python3 - "$CC_SWITCH_DB" "$DSH_HOME_DIR/.credentials.yaml" "$PROVIDER_NAME" <<'PY'
import json
import os
import sqlite3
import sys
import tempfile

database, destination, provider_name = sys.argv[1:]
connection = sqlite3.connect(database)
row = connection.execute(
    "select settings_config from providers where name = ? and app_type = 'codex'",
    (provider_name,),
).fetchone()
if row is None:
    raise SystemExit(f'cc-switch provider not found: {provider_name}')

settings = json.loads(row[0])
auth = settings.get('auth')
if not isinstance(auth, dict):
    raise SystemExit(f'cc-switch provider has no auth object: {provider_name}')
key = auth.get('OPENAI_API_KEY')
if not isinstance(key, str) or not key.strip():
    raise SystemExit(f'cc-switch provider has no OPENAI_API_KEY: {provider_name}')

parent = os.path.dirname(destination)
os.makedirs(parent, mode=0o700, exist_ok=True)
fd, temporary = tempfile.mkstemp(prefix='.credentials.', dir=parent, text=True)
try:
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        # JSON quoting is valid YAML and avoids accidental parsing of key text.
        stream.write('OPENAI_API_KEY: ' + json.dumps(key) + '\n')
    os.replace(temporary, destination)
finally:
    if os.path.exists(temporary):
        os.unlink(temporary)
PY

cp "$REPO_ROOT/profiles/yujp-web/cordis.patch.yml" "$DSH_HOME_DIR/profiles/web/cordis.patch.yml"
cp -R "$REPO_ROOT/profiles/yujp-web/presets/ppt-assistant" "$DSH_HOME_DIR/.agent-presets/"

# Keep the profile's external plugins isolated in the DSH profile directory.
cat > "$DSH_HOME_DIR/profiles/web/package.json" <<'JSON'
{
  "name": "dsh-profile-web",
  "private": true,
  "dependencies": {
    "@huiliyi37/dsh-office": "^0.2.1",
    "dsh-find-plugin": "^0.3.7",
    "dshmarket": "^1.17.1"
  },
  "dsh": {
    "profile": {
      "bundles": [
        "@deepseek-ai/dsh-base",
        "@deepseek-ai/dsh-web-app",
        "dshmarket",
        "dsh-find-plugin",
        "@huiliyi37/dsh-office"
      ]
    }
  }
}
JSON
cat > "$DSH_HOME_DIR/profiles/web/pnpm-workspace.yaml" <<'YAML'
packages:
  - .

nodeLinker: hoisted
autoInstallPeers: false
YAML

echo "Installed PPT profile into $DSH_HOME_DIR"
echo "Credential source: cc-switch provider $PROVIDER_NAME"
echo "Model route: codex-company / gpt-6.1-sol / high"
