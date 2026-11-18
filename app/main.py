from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user, hash_password, verify_password
from app.database import Base, engine, get_db
from app.models import Job, User
from app.schemas import JobCreate, JobResponse, UserCreate

app = FastAPI(title="Job Tracker API", description="Track your job applications.")

# Creates missing tables on startup. Fine for a small project; real projects use migrations (Alembic).
Base.metadata.create_all(bind=engine)


def get_own_job(job_id: int, db: Session, user: User) -> Job:
    """Fetch a job that belongs to the current user, or answer 404."""
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == user.id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/")
def root():
    return {"message": "Job Tracker API running"}


# ---------- Auth ----------

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=user_in.email, hashed_password=hash_password(user_in.password))
    db.add(user)
    db.commit()
    return {"message": "User created"}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    # Same error for "no such user" and "wrong password", so attackers can't probe which emails exist.
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}


# ---------- Jobs ----------

@app.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_job = Job(**job.model_dump(), user_id=user.id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@app.get("/jobs", response_model=list[JobResponse])
def get_jobs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Job).filter(Job.user_id == user.id).all()


@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_own_job(job_id, db, user)


@app.put("/jobs/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int, updated: JobCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    job = get_own_job(job_id, db, user)
    for field, value in updated.model_dump().items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job


@app.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    job = get_own_job(job_id, db, user)
    db.delete(job)
    db.commit()
