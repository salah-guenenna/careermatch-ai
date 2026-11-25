# CI/CD

The GitHub Actions workflow at `.github/workflows/ci.yml` runs on pushes to `main`/`master` and pull requests. It performs three checks:

1. Installs backend dependencies and runs Pytest.
2. Installs frontend dependencies and runs the Vite production build.
3. Validates the Docker Compose configuration.

To enable it, create a Git repository, commit the project, and push it to GitHub. The workflow does not deploy automatically; production deployment remains an explicit operator action using `docker-compose.prod.yml`.

