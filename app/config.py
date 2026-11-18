"""Settings read from environment variables.

Why: secrets and environment-specific values (passwords, keys, database
addresses) must never live in the code. The same code then runs on your
laptop, in Docker and in the cloud - only the environment changes.
"""
import os

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not set. Set it in your shell before starting the app, "
        "e.g. PowerShell:  $env:SECRET_KEY = 'some-long-random-string'"
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# SQLite by default for local development; later Docker will point this at Postgres.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jobs.db")
