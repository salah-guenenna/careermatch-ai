# Production deployment template

This repository includes `docker-compose.prod.yml`, a production frontend image, and Caddy for automatic HTTPS. Replace the example domains in `.env` with DNS names pointing to the server.

```bash
cp .env.example .env
# edit SECRET_KEY, database credentials, APP_DOMAIN, and API_DOMAIN
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec api alembic upgrade head
```

Open `https://APP_DOMAIN` and verify `https://API_DOMAIN/health/ready`. Caddy obtains and renews certificates automatically when DNS and ports 80/443 are configured. Keep `.env` private and back up the Postgres volume and `uploads/` data.

