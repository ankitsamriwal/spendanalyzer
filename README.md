# Devcontainer

Open this repo in GitHub Codespaces. This devcontainer:
- Enables Docker-in-Docker so `docker compose` works
- Forwards ports 8000 (API), 8501 (Admin), 5432 (Postgres)
- Auto-runs `make up` after creation (ignored if it fails the first time)

Tips:
- Add your secrets in **Codespaces ▸ Secrets** or create a `.env` from `.env.example`.
- Use Copilot Chat to scaffold workflows or code changes across the repo.
