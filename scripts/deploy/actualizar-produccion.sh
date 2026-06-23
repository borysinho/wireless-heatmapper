#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/wireless-heatmapper}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"

cd "$APP_DIR"

if [[ ! -f .env ]]; then
  echo "No existe $APP_DIR/.env. Copia .env.prod.example y completa los secretos." >&2
  exit 1
fi

mkdir -p certbot/conf certbot/www certbot/lib

docker compose --env-file .env -f "$COMPOSE_FILE" pull
docker compose --env-file .env -f "$COMPOSE_FILE" up -d db

echo "Aplicando migraciones Alembic..."
docker compose --env-file .env -f "$COMPOSE_FILE" run --rm backend python -m alembic upgrade head

if [[ -d certbot/conf/live ]]; then
  echo "Renovando certificado TLS si corresponde..."
  docker compose --env-file .env -f "$COMPOSE_FILE" --profile tls run --rm certbot || true
fi

docker compose --env-file .env -f "$COMPOSE_FILE" up -d --remove-orphans
docker image prune -f

echo "Estado de servicios:"
docker compose --env-file .env -f "$COMPOSE_FILE" ps
