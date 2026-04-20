FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /bin/

ADD . /app

WORKDIR /app

RUN uv sync --frozen --no-dev

CMD ["uv", "run" , "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]