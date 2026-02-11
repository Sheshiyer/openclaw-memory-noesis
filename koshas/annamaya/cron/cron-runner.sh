#!/usr/bin/env bash
# cron-runner.sh — stable shell wrapper for OpenClaw cron exec calls
# Usage:
#   cron-runner.sh "job-name" -- <command...>

set -euo pipefail

JOB_NAME="${1:-unnamed}"
shift || true

if [[ "${1:-}" != "--" ]]; then
  echo "Usage: cron-runner.sh <job-name> -- <command...>" >&2
  exit 2
fi
shift

TS="$(date +"%Y-%m-%d_%H%M%S")"
LOG_DIR="/Volumes/madara/2026/twc-vault/_System/cron/logs/${JOB_NAME}"
mkdir -p "$LOG_DIR"
LOG_PATH="${LOG_DIR}/${TS}.log"

# Stable PATH (cron/agent shells are inconsistent)
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:${PATH:-}"

RUNNER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ANNAMAYA_DIR="$(cd "${RUNNER_DIR}/.." && pwd)"

{
  echo "[cron-runner] job=${JOB_NAME} ts=${TS}"
  echo "[cron-runner] pwd=$(pwd)"
  echo "[cron-runner] cmd=$*"
  echo ""
  ENV_KV_CONFIG_PATH="${OPENCLAW_ENV_KV_CONFIG:-$HOME/.openclaw/config/env-kv.json}"
  if [[ -f "$ENV_KV_CONFIG_PATH" ]]; then
    ENV_KV_OUT="$(mktemp)"
    python3 "${ANNAMAYA_DIR}/scripts/cloudflare_kv.py" write-env-file --config "$ENV_KV_CONFIG_PATH" --out "$ENV_KV_OUT"
    set -a
    source "$ENV_KV_OUT"
    set +a
    rm -f "$ENV_KV_OUT"
  fi
  "$@"
} >"$LOG_PATH" 2>&1

echo "OK ${JOB_NAME} log=${LOG_PATH}"
