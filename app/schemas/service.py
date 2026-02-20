from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ServiceEntryCreate(BaseModel):
    date: date
    description: str
    hours: float
    reflection: str = ""


class ServiceEntryUpdate(BaseModel):
    date: Optional[date] = None
    description: Optional[str] = None
    hours: Optional[float] = None
    reflection: Optional[str] = None


class ServiceEntryResponse(BaseModel):
    id: UUID
    date: date
    description: str
    hours: float
    reflection: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
