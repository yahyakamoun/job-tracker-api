from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class JobStatus(str, Enum):
    """The only values a job's status may take. Anything else gets a 422 error."""

    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"


class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=8)


class JobCreate(BaseModel):
    company: str
    position: str
    status: JobStatus = JobStatus.applied
    notes: Optional[str] = None


class JobResponse(JobCreate):
    # Lets Pydantic read the values straight from a SQLAlchemy object.
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
