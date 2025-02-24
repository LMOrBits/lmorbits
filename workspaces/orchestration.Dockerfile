# FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu20.04
# FROM --platform=$BUILDPLATFORM
# FROM --platform=$BUILDPLATFORM python:3.11-slim

FROM zenmldocker/zenml
RUN apt-get update && apt-get install -y \
    curl 

COPY . /slmops
WORKDIR /
# RUN curl -LsSf https://astral.sh/uv/install.sh | bash 
# RUN /root/.local/bin/uv venv /venv
# ENV PATH="/venv/bin:$PATH"

RUN pip install uv
# RUN /root/.local/bin/uv pip install -e /slmops/packages/orchestration 
RUN uv pip install -e /slmops/packages/orchestration 
