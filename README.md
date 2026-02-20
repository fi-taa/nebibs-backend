# Nebibs Backend

FastAPI backend for Nebibs, connected to Supabase. Deploy on Render.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
```

Set in `.env`:

- `SUPABASE_URL` – from Supabase project settings (API URL)
- `SUPABASE_KEY` – anon key (or service role if you need server-side bypass)

Run:

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000  
- Docs: http://127.0.0.1:8000/docs

## Deploy on Render

1. Push this repo to GitHub (or GitLab).
2. In [Render](https://render.com): New → Web Service, connect the repo.
3. Render will use `render.yaml` if present (name: nebibs-backend, Python, uvicorn).
4. In the service Environment tab, add:
   - `SUPABASE_URL` = your Supabase project URL
   - `SUPABASE_KEY` = your Supabase anon (or service role) key
5. Deploy. The service will be at `https://nebibs-backend.onrender.com` (or the name you chose).

If you don’t use a blueprint, set manually:

- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Supabase schema

Run the schema once in your Supabase project (SQL Editor → paste contents of `supabase/schema.sql` → Run) to create tables: `learning_goals`, `experiments`, `service_entries`.

## Endpoints

- `GET /` – service info
- `GET /health` – health check
- `GET /docs` – **Swagger UI** (interactive API docs)
- `GET /openapi.json` – OpenAPI schema

### Learning goals
- `GET /learning/goals` – list all
- `GET /learning/goals/{id}` – get one
- `POST /learning/goals` – create
- `PATCH /learning/goals/{id}` – update
- `DELETE /learning/goals/{id}` – delete

### Experiments
- `GET /experiments` – list all
- `GET /experiments/{id}` – get one
- `POST /experiments` – create
- `PATCH /experiments/{id}` – update
- `DELETE /experiments/{id}` – delete

### Service entries
- `GET /service/entries` – list all
- `GET /service/entries/{id}` – get one
- `POST /service/entries` – create
- `PATCH /service/entries/{id}` – update
- `DELETE /service/entries/{id}` – delete

## Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Tests mock Supabase; no env vars needed. All endpoints are covered (list, get, create, update, delete, 404 cases).
