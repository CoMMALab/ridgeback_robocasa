"""Open an interactive MuJoCo viewer for the Ridgeback base MJCF."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import mujoco
import mujoco.viewer
from mjviser import Viewer


DEFAULT_MODEL = Path(__file__).resolve().parent / "mjcf" / "ridgeback_dual_panda.mjb"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Visualize the Ridgeback base in MuJoCo."
    )
    parser.add_argument(
        "model",
        nargs="?",
        type=Path,
        default=DEFAULT_MODEL,
        help=f"MJCF file to load (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the MJCF and exit without opening a window.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model_path = args.model.expanduser().resolve()
    if not model_path.is_file():
        raise SystemExit(f"MJCF file not found: {model_path}")

    model_str = str(model_path)
    if model_str.endswith(".xml"):
        model = mujoco.MjModel.from_xml_path(str(model_path))
    elif model_str.endswith(".mjb"):
        model = mujoco.MjModel.from_binary_path(str(model_path))
    else:
        raise SystemExit(f"Unsupported MJCF file provided")

    data = mujoco.MjData(model)
    Viewer(model, data).run()


if __name__ == "__main__":
    main()
