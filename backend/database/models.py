from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: uid("project"))
    title: Mapped[str] = mapped_column(String(200))
    schema_version: Mapped[str] = mapped_column(String(20), default="4.2")
    status: Mapped[str] = mapped_column(String(32), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc, onupdate=now_utc)

class Asset(Base):
    __tablename__ = "assets"
    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: uid("asset"))
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(32))
    uri: Mapped[str] = mapped_column(Text())
    version: Mapped[int] = mapped_column(Integer, default=1)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)

class Scene(Base):
    __tablename__ = "scenes"
    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: uid("scene"))
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    ordinal: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(200), default="")
    status: Mapped[str] = mapped_column(String(32), default="draft")
    data: Mapped[dict] = mapped_column(JSON, default=dict)
    __table_args__ = (UniqueConstraint("project_id", "ordinal", name="uq_scene_project_ordinal"),)

class Shot(Base):
    __tablename__ = "shots"
    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: uid("shot"))
    scene_id: Mapped[str] = mapped_column(ForeignKey("scenes.id", ondelete="CASCADE"), index=True)
    ordinal: Mapped[int] = mapped_column(Integer)
    duration: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(32), default="planned")
    data: Mapped[dict] = mapped_column(JSON, default=dict)
    __table_args__ = (UniqueConstraint("scene_id", "ordinal", name="uq_shot_scene_ordinal"),)

class RenderJob(Base):
    __tablename__ = "render_jobs"
    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: uid("job"))
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    shot_id: Mapped[str] = mapped_column(ForeignKey("shots.id", ondelete="CASCADE"), index=True)
    fingerprint: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    state: Mapped[str] = mapped_column(String(32), default="CREATED", index=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    lease_owner: Mapped[str | None] = mapped_column(String(128), nullable=True)
    lease_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    heartbeat_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc, onupdate=now_utc)

class GenerationRecord(Base):
    __tablename__ = "generation_records"
    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: uid("gen"))
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    shot_id: Mapped[str] = mapped_column(ForeignKey("shots.id", ondelete="CASCADE"), index=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("render_jobs.id", ondelete="CASCADE"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    provider: Mapped[str] = mapped_column(String(128))
    model: Mapped[str] = mapped_column(String(128))
    model_version: Mapped[str] = mapped_column(String(128), default="")
    prompt: Mapped[str] = mapped_column(Text(), default="")
    negative_prompt: Mapped[str] = mapped_column(Text(), default="")
    seed: Mapped[int | None] = mapped_column(Integer, nullable=True)
    parameters: Mapped[dict] = mapped_column(JSON, default=dict)
    references: Mapped[list] = mapped_column(JSON, default=list)
    artifact_uri: Mapped[str | None] = mapped_column(Text(), nullable=True)
    artifact_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    qc_result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    __table_args__ = (UniqueConstraint("shot_id", "version", name="uq_generation_shot_version"),)

class QAResult(Base):
    __tablename__ = "qa_results"
    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: uid("qa"))
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    shot_id: Mapped[str] = mapped_column(ForeignKey("shots.id", ondelete="CASCADE"), index=True)
    job_id: Mapped[str] = mapped_column(ForeignKey("render_jobs.id", ondelete="CASCADE"), index=True)
    generation_id: Mapped[str] = mapped_column(ForeignKey("generation_records.id", ondelete="CASCADE"), index=True)
    attempt: Mapped[int] = mapped_column(Integer)
    technical: Mapped[str] = mapped_column(String(16))
    visual: Mapped[str] = mapped_column(String(16))
    character: Mapped[str] = mapped_column(String(16))
    environment: Mapped[str] = mapped_column(String(16))
    temporal: Mapped[str] = mapped_column(String(16))
    timeline: Mapped[str] = mapped_column(String(16))
    decision: Mapped[str] = mapped_column(String(16), index=True)
    failure_codes: Mapped[list] = mapped_column(JSON, default=list)
    repair_plan: Mapped[dict] = mapped_column(JSON, default=dict)
    metrics: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
