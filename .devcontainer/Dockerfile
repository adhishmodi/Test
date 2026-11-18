FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /workspaces/Test

# Install the uv project manager used by the backend dependency workflow.
RUN python -m pip install --no-cache-dir uv==0.13.5

ENV UV_LINK_MODE=copy
