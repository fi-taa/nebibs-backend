from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.schemas.service import (
    ServiceEntryCreate,
    ServiceEntryResponse,
    ServiceEntryUpdate,
)
from app.supabase_client import get_supabase

router = APIRouter(prefix="/service", tags=["service"])


def _row_to_response(row: dict) -> ServiceEntryResponse:
    return ServiceEntryResponse(
        id=row["id"],
        date=row["date"],
        description=row["description"],
        hours=row["hours"],
        reflection=row.get("reflection", ""),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@router.get("/entries", response_model=list[ServiceEntryResponse])
async def list_entries():
    supabase = get_supabase()
    resp = supabase.table("service_entries").select("*").order("date", desc=True).execute()
    return [_row_to_response(row) for row in (resp.data or [])]


@router.get("/entries/{entry_id}", response_model=ServiceEntryResponse)
async def get_entry(entry_id: UUID):
    supabase = get_supabase()
    resp = supabase.table("service_entries").select("*").eq("id", str(entry_id)).execute()
    if not resp.data or len(resp.data) == 0:
        raise HTTPException(status_code=404, detail="Entry not found")
    return _row_to_response(resp.data[0])


@router.post("/entries", response_model=ServiceEntryResponse, status_code=201)
async def create_entry(body: ServiceEntryCreate):
    supabase = get_supabase()
    payload = {
        "date": body.date.isoformat(),
        "description": body.description,
        "hours": body.hours,
        "reflection": body.reflection,
    }
    resp = supabase.table("service_entries").insert(payload).execute()
    if not resp.data or len(resp.data) == 0:
        raise HTTPException(status_code=500, detail="Insert failed")
    return _row_to_response(resp.data[0])


@router.patch("/entries/{entry_id}", response_model=ServiceEntryResponse)
async def update_entry(entry_id: UUID, body: ServiceEntryUpdate):
    supabase = get_supabase()
    payload = body.model_dump(exclude_unset=True)
    if "date" in payload:
        payload["date"] = payload["date"].isoformat()
    if not payload:
        return await get_entry(entry_id)
    resp = supabase.table("service_entries").update(payload).eq("id", str(entry_id)).execute()
    if not resp.data or len(resp.data) == 0:
        raise HTTPException(status_code=404, detail="Entry not found")
    return _row_to_response(resp.data[0])


@router.delete("/entries/{entry_id}", status_code=204)
async def delete_entry(entry_id: UUID):
    supabase = get_supabase()
    resp = supabase.table("service_entries").delete().eq("id", str(entry_id)).execute()
    if resp.data is not None and len(resp.data) == 0:
        raise HTTPException(status_code=404, detail="Entry not found")
    return None
