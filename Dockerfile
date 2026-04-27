# Builder Stage
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./
COPY payer_website_autofiller ./payer_website_autofiller

# TEMPORARY for payers list
COPY payers_list.csv ./payers_list.csv

RUN uv build --wheel


# Run time stage
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/dist/*.whl ./

# TEMPORARY for payers list
COPY --from=builder /app/payers_list.csv ./payers_list.csv

RUN pip install --no-cache-dir *.whl
RUN playwright install --with-deps firefox

CMD ["uvicorn", "payer_website_autofiller.frontend.main:app", "--host", "0.0.0.0", "--port", "8000"]