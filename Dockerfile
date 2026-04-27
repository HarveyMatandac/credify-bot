FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen --no-dev
RUN uv run playwright install --with-deps firefox

COPY payer_website_autofiller ./payer_website_autofiller

# Temporary for payers list
COPY payers_list.csv ./payers_list.csv

CMD ["uv", "run" , "uvicorn", "payer_website_autofiller.frontend.main:app", "--host", "0.0.0.0", "--port", "8000"]