# Mini SQL Agent

Agentic Text-to-SQL application using Claude Haiku. Ask natural language questions and get SQL queries executed against a PostgreSQL `classicmodels` database.

## Prerequisites

- Docker and Docker Compose
- An Anthropic API key

## Setup

1. Copy the example env file and add your API key:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and replace `your-anthropic-api-key-here` with your actual Anthropic API key.

## Run

```bash
docker compose up --build
```

This starts three services:

| Service    | URL                          |
|------------|------------------------------|
| API        | http://localhost:8001         |
| Streamlit  | http://localhost:8501         |
| PostgreSQL | localhost:5433               |

## Usage

**Streamlit UI** - Open http://localhost:8501 in your browser and ask questions in plain English.

**API** - Send a POST request:

```bash
curl -X POST http://localhost:8001/agent/sql \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers are in France?"}'
```

## Stop

```bash
docker compose down
```
