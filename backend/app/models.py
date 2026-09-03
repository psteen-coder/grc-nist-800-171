from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    REVIEWER = "reviewer"
    ANALYST = "analyst"
    EVIDENCE_GATHERER = "evidence_gatherer"

class StatusEnum(str, enum.Enum):
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.ANALYST)
    created_at = Column(DateTime, default=datetime.utcnow)

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    owner = Column(String)
    cui_categories = Column(String)
    system_boundary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    assessments = relationship("Assessment", back_populates="application")

class Control(Base):
    __tablename__ = "controls"
    id = Column(Integer, primary_key=True, index=True)
    control_id = Column(String, unique=True, index=True)  # e.g. "3.1.1"
    family = Column(String)
    short_text = Column(Text)
    full_text = Column(Text)
    testing_criteria = Column(Text)

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    control_id = Column(Integer, ForeignKey("controls.id"))
    status = Column(Enum(StatusEnum))
    explanation = Column(Text)
    evidence_blob = Column(Text)  # base64 or path for now
    assessed_by = Column(String)
    assessed_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="assessments")