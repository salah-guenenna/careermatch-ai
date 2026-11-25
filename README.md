# CareerMatch AI

CareerMatch AI is a modular-monolith SaaS application for CV analysis and explainable job matching.

## Phase 1 status

This repository currently contains the runnable foundation: a FastAPI backend with configuration and a health endpoint, a Vite React TypeScript frontend, PostgreSQL wiring through SQLAlchemy, Docker Compose, and an initial automated backend test. Product modules are intentionally introduced in later phases.

See [`docs/architecture.md`](docs/architecture.md) for the target module boundaries and phased roadmap.

## Run

Copy `.env.example` to `.env`, then run `docker compose up --build`. Open `http://localhost:5173`, API health at `http://localhost:8000/health`, and Swagger at `http://localhost:8000/docs`.

For a local backend run: `cd backend`, create a Python 3.11 virtual environment, `pip install -r requirements.txt`, then `uvicorn app.main:app --reload`. The backend defaults to SQLite when `DATABASE_URL` is not set; Compose uses PostgreSQL.

Verify with `cd backend && pytest`.

## Phase 3 API examples

Register or sign in through Swagger to obtain a bearer token. Then use `POST /cvs/upload` with a multipart PDF and `POST /jobs` with `{ "title": "Backend Engineer", "company": "Example", "description": "..." }`. Uploaded PDFs are limited to 5 MB, stored under `uploads/`, and rejected when they contain no selectable text.

## Phase 4 analysis example

After creating a CV and job offer, call `POST /analyses` with `{ "cv_id": 1, "job_offer_id": 1 }`. The response contains a reproducible score, component scores, matched and missing skills, an explanation, and recommendations. The baseline uses a controlled skills vocabulary plus TF-IDF cosine similarity and does not score demographic or sensitive attributes.

