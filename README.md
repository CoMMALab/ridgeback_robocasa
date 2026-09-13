# Ridgeback Environment
This repository contains all code necessary to run the Clearpath Robotics Ridgeback mobile base both in real life and in sim. It also has support for attached robot arms, such as the Franka Emika Panda arms and a selection of UR models.

## Setup
This project uses `uv` for dependency management. Run the following command to install `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify that your setup works by running:
```bash
uv run python3 visualize_ridgeback
```

This should show an MjViser visualization of a simulated ridgeback base with two mounted Franka Emika Panda arms.

## References
- https://github.com/ridgeback/ridgeback
- https://github.com/ridgeback/ridgeback_manipulation