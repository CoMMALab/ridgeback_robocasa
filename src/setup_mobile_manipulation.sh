#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$project_dir"

export MS_ASSET_DIR="$project_dir/assets"
mkdir -p "$MS_ASSET_DIR"

uv sync
# ManiSkill's MS-HAB branch uses legacy setup.py metadata, so install it after
# uv sync and use `uv run --no-sync` for launch commands.
uv pip install --editable ./vendor/ManiSkill

uv run --no-sync python -m mani_skill.utils.download_asset \
  partnet_mobility_cabinet -y

echo "Setup complete. Launch with:"
echo "  uv run --no-sync python maniskill_test.py"
