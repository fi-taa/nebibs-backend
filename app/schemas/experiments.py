from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

ExperimentStatus = str


class ExperimentCreate(BaseModel):
    title: str
    description: str = ""
    dependencies: List[str] = Field(default_factory=list)
    next_action: str = ""
    status: ExperimentStatus = "not_started"
    notes: str = ""


class ExperimentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    dependencies: Optional[List[str]] = None
    next_action: Optional[str] = None
    status: Optional[ExperimentStatus] = None
    notes: Optional[str] = None


class ExperimentResponse(BaseModel):
    id: UUID
    title: str
    description: str
    dependencies: List[str]
    next_action: str
    status: str
    notes: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
