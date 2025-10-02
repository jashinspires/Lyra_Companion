# Lyra Backend

Lyra's backend provides the FastAPI services that power the empathetic mental health companion experience. This backend currently runs fully in-memory for journals, mood logs, and conversation safety, making it easy to prototype without external databases.

## Features

- **Chat orchestration** with safety checks, emotion estimation, and coping suggestions
- **Journaling API** for creating entries, listing them, and generating summaries
- **Mood tracking** to log daily mood intensity and review simple trends
- **Safety assessment** endpoint for explicit crisis detection checks
- **Health monitoring** routes for readiness probes

## Project layout

```
backend/
  app/
    api/routes/      # FastAPI routers (chat, journal, mood, safety, health)
    core/            # Settings, logging, and lifecycle events
    services/        # In-memory services for conversation, journal, mood, safety
    schemas/         # Pydantic models shared by routes/services
    main.py          # FastAPI factory + router registration
  tests/             # Pytest suite exercising public endpoints
  requirements.txt  # Runtime dependencies
  requirements-dev.txt # Runtime + testing dependencies
  Dockerfile         # Container image definition
  .env.example       # Sample configuration values
```

## Getting started

1. Create a virtual environment and install dependencies:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r requirements-dev.txt
   ```

2. Copy `.env.example` to `.env` and adjust any sensitive values (OpenAI key, Pinecone index, etc.).
3. Launch the API locally:

   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Visit `http://127.0.0.1:8000/docs` for interactive documentation.

## Running tests

```powershell
pytest
```

The suite covers health checks, chat orchestration (with fallback replies), journaling flows, mood tracking trends, and safety detection logic.

## Docker

Build and run the containerized API:

```powershell
# Build image
 docker build -t lyra-backend .

# Run container
 docker run -p 8000:8000 --env-file .env lyra-backend
```

## Next steps

- Swap in a persistent data store (e.g., MongoDB) for journals and mood logs
- Integrate real LLM responses with structured safety moderation once API keys are configured
- Harden analytics/telemetry and introduce background task queues for long-running jobs
