FROM ubuntu:jammy

LABEL maintainer="Lukas Lüftinger <lukas.lueftinger@outlook.com>"
LABEL description="A Docker image for lolcatt"

SHELL ["/bin/bash", "-c"]
ENV PATH=$PATH:/opt/venv/bin
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    make \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Install Python dependencies
ADD . /opt/lolcatt
RUN --mount=type=cache,target=/root/.cache/pip \
    cd /opt/lolcatt \
    && source /opt/venv/bin/activate \
    && make install
