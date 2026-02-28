FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=builder /install /usr/local
COPY . /app

RUN mkdir -p /app/staticfiles /app/media && chown -R app:app /app

USER app

ENV DJANGO_SETTINGS_MODULE=devops_project.settings

CMD ["gunicorn", "devops_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

