from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.schemas.experiments import (
    ExperimentCreate,
    ExperimentResponse,
    ExperimentUpdate,
)
from app.supabase_client import get_supabase

router = APIRouter(prefix="/experiments", tags=["experiments"])


def _row_to_response(row: dict) -> ExperimentResponse:
    return ExperimentResponse(
        id=row["id"],
        title=row["title"],
        description=row.get("description", ""),
        dependencies=row.get("dependencies") or [],
        next_action=row.get("next_action", ""),
        status=row.get("status", "not_started"),
        notes=row.get("notes", ""),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@router.get("", response_model=list[ExperimentResponse])
async def list_experiments():
    supabase = get_supabase()
    resp = supabase.table("experiments").select("*").order("created_at", desc=True).execute()
    return [_row_to_response(row) for row in (resp.data or [])]


@router.get("/{experiment_id}", response_model=ExperimentResponse)
async def get_experiment(experiment_id: UUID):
    supabase = get_supabase()
    resp = supabase.table("experiments").select("*").eq("id", str(experiment_id)).execute()
    if not resp.data or len(resp.data) == 0:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return _row_to_response(resp.data[0])


@router.post("", response_model=ExperimentResponse, status_code=201)
async def create_experiment(body: ExperimentCreate):
    supabase = get_supabase()
    payload = {
        "title": body.title,
        "description": body.description,
        "dependencies": body.dependencies,
        "next_action": body.next_action,
        "status": body.status,
        "notes": body.notes,
    }
    resp = supabase.table("experiments").insert(payload).execute()
    if not resp.data or len(resp.data) == 0:
        raise HTTPException(status_code=500, detail="Insert failed")
    return _row_to_response(resp.data[0])


@router.patch("/{experiment_id}", response_model=ExperimentResponse)
async def update_experiment(experiment_id: UUID, body: ExperimentUpdate):
    supabase = get_supabase()
    payload = body.model_dump(exclude_unset=True)
    if not payload:
        return await get_experiment(experiment_id)
    resp = supabase.table("experiments").update(payload).eq("id", str(experiment_id)).execute()
    if not resp.data or len(resp.data) == 0:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return _row_to_response(resp.data[0])


@router.delete("/{experiment_id}", status_code=204)
async def delete_experiment(experiment_id: UUID):
    supabase = get_supabase()
    resp = supabase.table("experiments").delete().eq("id", str(experiment_id)).execute()
    if resp.data is not None and len(resp.data) == 0:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return None
