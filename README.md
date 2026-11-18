# Job Tracker API

A REST API to track job applications. Users register, log in with a JWT token and manage their own applications (company, position, status, notes). Each user only ever sees their own data.

**Tech stack:** Python, FastAPI, SQLAlchemy, SQLite (PostgreSQL planned), JWT auth with bcrypt-hashed passwords.

## Run locally

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

$env:SECRET_KEY = "some-long-random-string"
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API documentation.

## Endpoints

| Method | Path | Auth | What it does |
| --- | --- | --- | --- |
| POST | `/register` | – | Create a user (JSON: `email`, `password` ≥ 8 chars) |
| POST | `/login` | – | Get a JWT access token |
| GET | `/jobs` | Bearer token | List your jobs |
| POST | `/jobs` | Bearer token | Add a job |
| GET | `/jobs/{id}` | Bearer token | Get one job |
| PUT | `/jobs/{id}` | Bearer token | Update a job |
| DELETE | `/jobs/{id}` | Bearer token | Delete a job |

Job status is one of: `applied`, `interview`, `offer`, `rejected`.

## Project structure

```
app/
  main.py      # routes
  auth.py      # password hashing, JWT creation and checking
  config.py    # settings from environment variables
  database.py  # database connection and sessions
  models.py    # database tables (SQLAlchemy)
  schemas.py   # request/response shapes (Pydantic)
```

## Roadmap

- [ ] Automated tests (pytest)
- [ ] Docker + docker-compose with PostgreSQL
- [ ] CI with GitHub Actions
- [ ] Deployment to Azure
