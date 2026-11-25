#!/usr/bin/env bash
set -euo pipefail
mkdir -p backups
stamp=$(date +%Y%m%d-%H%M%S)
docker compose exec -T db pg_dump -U "${POSTGRES_USER:-careermatch}" -d "${POSTGRES_DB:-careermatch}" > "backups/careermatch-${stamp}.sql"
if [ -d uploads ]; then tar -czf "backups/uploads-${stamp}.tar.gz" uploads; fi
echo "Backup complete: backups/careermatch-${stamp}.sql"

