"""Attach an interchangeable manipulator MJCF to the reusable Ridgeback base."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import mujoco


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manipulator", type=Path, help="Standalone manipulator MJCF")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Compiled .mjb output")
    parser.add_argument("--prefix", default="manipulator_", help="Prefix for imported names")
    args = parser.parse_args()

    mjcf_dir = Path(__file__).resolve().parent
    output = args.output.resolve()
    if output.suffix != ".mjb":
        parser.error("output must end in .mjb; attached child asset paths are finalized at compile time")
    base = mujoco.MjSpec.from_file(str(mjcf_dir / "ridgeback_base.xml"))
    manipulator = mujoco.MjSpec.from_file(str(args.manipulator.resolve()))
    mount = base.frame("manipulator_mount")
    if mount is None:
        raise RuntimeError("ridgeback_base.xml has no manipulator_mount frame")

    # Finalize nested attachments/keyframes before importing the module again.
    manipulator.compile()
    base.attach(manipulator, frame=mount, prefix=args.prefix)

    # ridgeback_base.xml intentionally keeps portable paths relative to mjcf/.
    previous_dir = Path.cwd()
    try:
        os.chdir(mjcf_dir)
        portable_meshdir = base.meshdir
        base.meshdir = str(mjcf_dir / "meshes")
        model = base.compile()
        base.meshdir = portable_meshdir
        output.parent.mkdir(parents=True, exist_ok=True)
        mujoco.mj_saveModel(model, str(output))
    finally:
        os.chdir(previous_dir)


if __name__ == "__main__":
    main()
