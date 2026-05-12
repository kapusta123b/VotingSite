FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    gcc \
    netcat-openbsd \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY backend/ .

RUN chmod +x /app/entrypoint.sh

RUN useradd -s /bin/sh -u 1234 nonroot
RUN chown -R nonroot:nonroot /app

USER root

ENTRYPOINT [ "/app/entrypoint.sh" ]