#!/usr/bin/env bash
# Idempotent Cloud Agent install script for code_learning.
# Safe to run repeatedly: provisions venv support once, then refreshes deps.
set -euo pipefail

ensure_venv_support() {
  # The default Cloud Agent image ships python3 without the venv/ensurepip
  # module. Provision it once; apt-get install is a no-op when already present.
  if python3 -c "import ensurepip" >/dev/null 2>&1; then
    return 0
  fi
  echo "Provisioning python venv support (python3-venv)..."
  sudo apt-get update -qq
  sudo apt-get install -y -qq python3-venv || sudo apt-get install -y -qq python3.12-venv
}

ensure_venv_support

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
