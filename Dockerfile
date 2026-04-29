# Base Stage
FROM python:3.12-slim AS base
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/

WORKDIR /app

# Builder Stage
FROM base AS builder

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

RUN uv venv && uv sync --frozen --no-dev

COPY payer_website_autofiller ./payer_website_autofiller

# RUN uv build --wheel


# Runtime stage
FROM base AS api

RUN uvx patchright install --with-deps firefox

# COPY --from=builder /app/dist/*.whl ./
COPY --from=builder /app/.venv /app/.venv

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# RUN uv venv && uv pip install --no-cache-dir *.whl

# CMD ["uv", "run", "uvicorn", "payer_website_autofiller.frontend.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "payer_website_autofiller.frontend.main:app", "--host", "0.0.0.0", "--port", "8000"]