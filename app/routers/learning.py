from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.schemas.learning import (
    LearningGoalCreate,
    LearningGoalResponse,
    LearningGoalUpdate,
)
from app.supabase_client import get_supabase

router = APIRouter(prefix="/learning", tags=["learning"])


def _row_to_response(row: dict) -> LearningGoalResponse:
    return LearningGoalResponse(
        id=row["id"],
        title=row["title"],
        target_hours=row.get("target_hours"),
        progress_percent=row.get("progress_percent", 0),
        notes=row.get("notes", ""),
        resources=row.get("resources") or [],
        weekly_hours=row.get("weekly_hours") or [],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@router.get("/goals", response_model=list[LearningGoalResponse])
async def list_goals():
    supabase = get_supabase()
    resp = supabase.table("learning_goals").select("*").order("created_at", desc=True).execute()
    return [_row_to_response(row) for row in (resp.data or [])]


@router.get("/goals/{goal_id}", response_model=LearningGoalResponse)
async def get_goal(goal_id: UUID):
    supabase = get_supabase()
    resp = supabase.table("learning_goals").select("*").eq("id", str(goal_id)).execute()
    if not resp.data or len(resp.data) == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    return _row_to_response(resp.data[0])


@router.post("/goals", response_model=LearningGoalResponse, status_code=201)
async def create_goal(body: LearningGoalCreate):
    supabase = get_supabase()
    payload = {
        "title": body.title,
        "target_hours": body.target_hours,
        "progress_percent": 0,
        "notes": body.notes,
        "resources": [],
        "weekly_hours": [],
    }
    try:
        resp = supabase.table("learning_goals").insert(payload).execute()
        if not resp.data or len(resp.data) == 0:
            raise HTTPException(status_code=500, detail="Insert failed")
        return _row_to_response(resp.data[0])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.patch("/goals/{goal_id}", response_model=LearningGoalResponse)
async def update_goal(goal_id: UUID, body: LearningGoalUpdate):
    supabase = get_supabase()
    payload = body.model_dump(exclude_unset=True)
    if not payload:
        return await get_goal(goal_id)
    resp = supabase.table("learning_goals").update(payload).eq("id", str(goal_id)).execute()
    if not resp.data or len(resp.data) == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    return _row_to_response(resp.data[0])


@router.delete("/goals/{goal_id}", status_code=204)
async def delete_goal(goal_id: UUID):
    supabase = get_supabase()
    resp = supabase.table("learning_goals").delete().eq("id", str(goal_id)).execute()
    if resp.data is not None and len(resp.data) == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    return None
