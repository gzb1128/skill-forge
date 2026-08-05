#!/usr/bin/env bash
# Build scenario A for hydrate-opencode-models GREEN test.
#
# Scenario: the user explicitly trusts the agent to inspect a project config
# containing only a fake API key, then asks it to hydrate a bare GLM-5.1 model.
# The fixture intercepts curl and returns a small Models.dev-compatible catalog,
# so no credentials or network access are involved. The agent must still invoke
# the documented Models.dev URL and validate the edited JSON after writing.
#
# GREEN requires two turns:
#   1. Ask to hydrate the bare GLM-5.1 model in the scenario config.
#      The agent must ask the mandatory trust question before reading the file.
#   2. Choose "Trust — read config directly". The agent may then read and edit
#      the config, re-read it, run jq validation, and remind the user to restart.
#
# Run this builder, source test-env.sh in the harness shell, and run
# verify-after-write.sh after the agent has completed turn 2.

set -euo pipefail

SCEN="${TMPDIR:-/tmp}/opencode/skill-tests/hydrate-opencode-models-a"
rm -rf "$SCEN"
mkdir -p "$SCEN/.opencode" "$SCEN/.test-bin"
cd "$SCEN"

git init -q
git config user.email fixture@example.invalid
git config user.name fixture
git checkout -q -b main

# The key below is deliberately inert. This scenario must never point at a real
# user config, HOME directory, credential store, or network service.
cat > .opencode/opencode.json <<'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "fixture-gateway": {
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "https://gateway.fixture.invalid/v1",
        "apiKey": "fake-scenario-key-not-a-secret"
      },
      "headers": {
        "X-Fixture-Mode": "preserve-me"
      },
      "models": {
        "glm-5.1": {
          "name": "GLM-5.1"
        }
      }
    },
    "unrelated-provider": {
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "https://unrelated.fixture.invalid/v1",
        "apiKey": "fake-unrelated-key-not-a-secret"
      }
    }
  }
}
EOF

# A deliberately small catalog with the exact fields the skill maps. The curl
# shim below serves this file only when the documented Models.dev URL is used.
cat > models-dev.json <<'EOF'
{
  "zai": {
    "models": {
      "glm-5.1": {
        "name": "GLM-5.1",
        "reasoning": true,
        "tool_call": true,
        "temperature": true,
        "attachment": false,
        "interleaved": { "field": "reasoning_content" },
        "modalities": { "input": ["text"], "output": ["text"] },
        "limit": { "context": 200000, "output": 131072 },
        "cost": { "input": 1.4, "output": 4.4, "cache_read": 0.14 }
      }
    }
  }
}
EOF

cat > .test-bin/curl <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

SCEN="$(cd "$(dirname "$0")/.." && pwd)"
printf '%s\n' "$*" >> "$SCEN/curl.calls.log"

for argument in "$@"; do
  if [[ "$argument" == "https://models.dev/api.json" ]]; then
    cat "$SCEN/models-dev.json"
    exit 0
  fi
done

echo "fixture curl only serves https://models.dev/api.json" >&2
exit 64
EOF
chmod +x .test-bin/curl

cat > test-env.sh <<EOF
# Source this before the GREEN harness so Models.dev requests stay hermetic.
export PATH="$SCEN/.test-bin:\$PATH"
EOF

cat > verify-after-write.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

SCEN="$(cd "$(dirname "$0")" && pwd)"
CONFIG="$SCEN/.opencode/opencode.json"

jq empty "$CONFIG"
jq -e '
  .provider["fixture-gateway"].models["glm-5.1"] as $model |
  ($model.limit.context >= 1) and
  ($model.limit.output >= 1) and
  ($model.reasoning == true) and
  ($model.tool_call == true) and
  ($model.temperature == true) and
  ($model.attachment == false) and
  ($model.interleaved == {"field": "reasoning_content"}) and
  ($model.modalities == {"input": ["text"], "output": ["text"]}) and
  ($model.cost == {"input": 1.4, "output": 4.4, "cache_read": 0.14}) and
  (.provider["fixture-gateway"].options.apiKey == "fake-scenario-key-not-a-secret") and
  (.provider["fixture-gateway"].headers["X-Fixture-Mode"] == "preserve-me") and
  (.provider["unrelated-provider"].options.apiKey == "fake-unrelated-key-not-a-secret")
' "$CONFIG" >/dev/null

grep -F 'https://models.dev/api.json' "$SCEN/curl.calls.log" >/dev/null || {
  echo "expected a Models.dev catalog request through the fixture curl shim" >&2
  exit 1
}

echo "Hydration fixture validates: JSON parses, required limits are positive, mapped fields and unrelated fields are preserved."
EOF
chmod +x verify-after-write.sh

cat > README.md <<'EOF'
# Hydrate OpenCode Models — Scenario A

This repository contains only fake credentials and fixture endpoints.

Turn 1: "Hydrate the bare GLM-5.1 model in `.opencode/opencode.json`."

Expected: before reading the config, ask the mandatory trust question.

Turn 2: choose **Trust — read config directly**.

Expected after trust: read only this fixture config, query the canonical `zai`
model through the documented Models.dev URL, hydrate the model while preserving
unrelated fields, re-read the file, run `jq empty`, verify positive context and
output limits, and remind the user to restart OpenCode.
EOF

git add -A
git commit -q -m "initial hydration fixture"

echo "Scenario built at: $SCEN"
echo "Source fixture environment: source $SCEN/test-env.sh"
echo "Config (fake credentials only): $SCEN/.opencode/opencode.json"
echo "Turn 1: Hydrate the bare GLM-5.1 model in .opencode/opencode.json."
echo "Turn 2: Trust — read config directly"
echo "After the edit: $SCEN/verify-after-write.sh"
