# Ridgeback Environment
This repository contains all code necessary to run the Clearpath Robotics Ridgeback mobile base both in real life and in sim. It also has support for attached robot arms, such as the Franka Emika Panda arms and a selection of UR models.

## Setup
This project uses `uv` for dependency management. Run the following command to install `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

This project also uses submodules. Ensure that you initialize all submodules via the following:
```
git submodule update --init --recursive
```

Verify that your setup works by running the robocasa demo with the Ridgeback Dual Panda configuration:
```bash
uv run python3 -m robocasa.demos.demo_kitchen_scenes --robot RidgebackDualPanda
```

This will pull up a visualization of the Ridgeback Dual Panda configuration in a kitchen layout of your choosing. You can verify that the system works as expected with keyboard teleoperated control - the `b` key toggles whether you control the base or arms, and the arrow keys apply your control to the robot. The `o` and `p` keys control the base's yaw when base control is toggled on.

## References
- https://github.com/ridgeback/ridgeback
- https://github.com/ridgeback/ridgeback_manipulation