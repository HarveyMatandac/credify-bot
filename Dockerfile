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

# Runtime stage
FROM base AS api

RUN uvx patchright install --with-deps chromium

COPY --from=builder /app/.venv /app/.venv

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "payer_website_autofiller.frontend.main:app", "--host", "0.0.0.0", "--port", "8000"]