#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [[ ! -f backend/.env ]]; then
  echo "backend/.env not found — copying from backend/.env.example"
  cp backend/.env.example backend/.env
fi

exec docker compose up --build "$@"
