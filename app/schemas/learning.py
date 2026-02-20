from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class WeeklyHoursItem(BaseModel):
    week_key: str
    hours: float


class LearningGoalCreate(BaseModel):
    title: str
    target_hours: Optional[float] = None
    notes: str = ""


class LearningGoalUpdate(BaseModel):
    title: Optional[str] = None
    target_hours: Optional[float] = None
    progress_percent: Optional[float] = None
    notes: Optional[str] = None
    resources: Optional[List[str]] = None
    weekly_hours: Optional[List[WeeklyHoursItem]] = None


class LearningGoalResponse(BaseModel):
    id: UUID
    title: str
    target_hours: Optional[float]
    progress_percent: float
    notes: str
    resources: List[str]
    weekly_hours: List[dict]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
