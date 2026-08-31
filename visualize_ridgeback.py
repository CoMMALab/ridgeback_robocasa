"""Open an interactive MuJoCo viewer for the Ridgeback base MJCF."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import mujoco
import mujoco.viewer


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
        "--simulate",
        action="store_true",
        help="Run physics while the viewer is open (the default shows a static model).",
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
    mujoco.mj_forward(model, data)

    if args.check:
        print(
            f"Loaded {model_path} "
            f"({model.nbody} bodies, {model.ngeom} geoms, {model.njnt} joints)."
        )
        return

    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            frame_start = time.monotonic()
            if args.simulate:
                mujoco.mj_step(model, data)
            viewer.sync()

            if args.simulate:
                remaining = model.opt.timestep - (time.monotonic() - frame_start)
                if remaining > 0:
                    time.sleep(remaining)
            else:
                time.sleep(1 / 60)


if __name__ == "__main__":
    main()
