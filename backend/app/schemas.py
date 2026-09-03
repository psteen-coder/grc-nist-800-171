from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "admin"
    REVIEWER = "reviewer"
    ANALYST = "analyst"
    EVIDENCE_GATHERER = "evidence_gatherer"

class StatusEnum(str, Enum):
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"

# User
class UserBase(BaseModel):
    username: str
    role: RoleEnum = RoleEnum.ANALYST

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Application
class ApplicationBase(BaseModel):
    name: str
    description: Optional[str] = None
    owner: Optional[str] = None
    cui_categories: Optional[str] = None
    system_boundary: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationOut(ApplicationBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# Assessment
class AssessmentBase(BaseModel):
    status: StatusEnum
    explanation: Optional[str] = None
    evidence_blob: Optional[str] = None   # base64 for now

class AssessmentCreate(AssessmentBase):
    application_id: int
    control_id: int

class AssessmentOut(AssessmentBase):
    id: int
    assessed_by: Optional[str] = None
    assessed_at: datetime
    class Config:
        from_attributes = True

# Control (read-only for now)
class ControlOut(BaseModel):
    id: int
    control_id: str
    family: str
    short_text: str
    full_text: Optional[str] = None
    testing_criteria: Optional[str] = None
    class Config:
        from_attributes = True

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str