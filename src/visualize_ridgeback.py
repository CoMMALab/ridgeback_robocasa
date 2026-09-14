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
    # Viewer(model, data).run()  # <-- REQUIRES MJVISER, MUJOCO 3.13.1 WHICH IS INCOMPATIBLE WITH ROBOSUITE/ROBOCASA

    with mujoco.viewer.launch_passive(model, data) as viewer:
        # Close the viewer cleanly upon loop completion or script exit
        while viewer.is_running():
            step_start = time.time()

            # Place your custom controllers, forces, or logic here
            # Example: data.ctrl[0] = 1.0

            # Step the physics forward
            mujoco.mj_step(model, data)

            # Synchronize viewer markers and physics state
            viewer.sync()

            # Constrain loop timing to match real-time physics simulation
            time_now = time.time()
            time_until_next_step = model.opt.timestep - (time_now - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)


if __name__ == "__main__":
    main()
