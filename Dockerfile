FROM ghcr.io/commalab/ros-noetic

# uv install
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /comma