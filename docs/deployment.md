# Deployment and verification

## Local production-like run

Copy `.env.example` to `.env`, replace `SECRET_KEY` with a long random value, and run `docker compose up -d --build`. Verify `http://localhost:8000/health/ready`, `http://localhost:8000/docs`, and `http://localhost:5173`.

## Database migrations

The API creates tables for a first local run. For controlled environments, run migrations from the API container:

```bash
docker compose exec api alembic upgrade head
```

## Security checklist

- Set a unique `SECRET_KEY` through the environment.
- Keep PostgreSQL private to the application network in production.
- Put the API behind HTTPS and a reverse proxy.
- Keep uploaded files outside the public web root and back them up separately.
- Do not commit `.env`, `uploads/`, tokens, or CV files.
- Restrict CORS origins to the deployed frontend hostname.

## Optional semantic matching

The default matcher is deterministic and requires no model download. To enable semantic similarity, install the optional requirements inside the API image with `pip install -r requirements-semantic.txt`, set `ENABLE_SEMANTIC_MATCHING=true`, and rebuild. The first analysis downloads `all-MiniLM-L6-v2`; plan disk space and startup time accordingly. If the optional package is absent, semantic matching remains disabled rather than inventing a score.

On Windows, use 64-bit Python. Verify with `python -c "import platform; print(platform.architecture())"`; it must print `('64bit', ...)`. Python `cp310-win32` cannot install the required SciPy/PyTorch wheels. Create a clean virtual environment with Python 3.11 or newer before installing the optional requirements.

## Functional smoke test

1. Register or log in.
2. Upload a text-based PDF CV.
3. Create a job offer.
4. Create an analysis and confirm the score, matched skills, missing skills, and recommendations.
5. Download `/analyses/{id}/report` and check the PDF.

