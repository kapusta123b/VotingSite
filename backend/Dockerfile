# syntax=docker/dockerfile:1

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    netcat-openbsd \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN useradd \
    --system \
    --uid 1234 \
    --create-home \
    --shell /bin/sh \
    nonroot

COPY --chown=nonroot:nonroot backend/ /app/

RUN chmod 755 entrypoint.sh

USER nonroot

EXPOSE 8000

ENTRYPOINT [ "/app/entrypoint.sh" ]