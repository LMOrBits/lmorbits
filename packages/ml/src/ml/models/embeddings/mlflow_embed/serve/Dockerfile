FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync

COPY . .
EXPOSE 1111

ENTRYPOINT [ "uv", "run", "python", "serve.py", "--params-file", "${PARAMS_FILE:-/app/params.yaml}" ]

