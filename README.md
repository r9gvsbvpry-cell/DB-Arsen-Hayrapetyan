Project: Project Management REST API

Overview
- Implements a small FastAPI service with PostgreSQL via SQLAlchemy.
- Models: Project, Assignment (Поручение), Worker (Работник).
- Uses Alembic for migrations. Includes a JSONB field + pg_trgm index for regex search.

Quick start (with Docker Compose)

1) Start Postgres:

```powershell
docker-compose up -d
```

2) Create DB and owner (adjust env vars):

```powershell
python create_db.py
```

3) Install deps and run app:

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4) Use `seed/seed.py` to populate the DB through the REST API.

Notes
- Alembic folder contains two example migrations: initial schema and adding JSON field + index.
- The `init_db.sql` demonstrates how to create database and owner with psql.