from unittest.mock import Mock, patch
from uuid import uuid4


def _goal_row(goal_id=None, title="Learn Python", **kwargs):
    row = {
        "id": str(goal_id or uuid4()),
        "title": title,
        "target_hours": 10.0,
        "progress_percent": 0,
        "notes": "",
        "resources": [],
        "weekly_hours": [],
        "created_at": "2025-01-01T00:00:00",
        "updated_at": "2025-01-01T00:00:00",
    }
    row.update(kwargs)
    return row


@patch("app.routers.learning.get_supabase")
def test_list_goals_empty(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.select.return_value.order.return_value.execute.return_value = Mock(data=[])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.get("/learning/goals")
    assert r.status_code == 200
    assert r.json() == []


@patch("app.routers.learning.get_supabase")
def test_list_goals_returns_items(mock_get_supabase, client):
    row = _goal_row()
    mock_table = Mock()
    mock_table.select.return_value.order.return_value.execute.return_value = Mock(data=[row])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.get("/learning/goals")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["title"] == row["title"]
    assert data[0]["id"] == row["id"]


@patch("app.routers.learning.get_supabase")
def test_get_goal_ok(mock_get_supabase, client):
    goal_id = uuid4()
    row = _goal_row(goal_id=goal_id)
    mock_table = Mock()
    mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[row])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.get(f"/learning/goals/{goal_id}")
    assert r.status_code == 200
    assert r.json()["id"] == str(goal_id)
    assert r.json()["title"] == row["title"]


@patch("app.routers.learning.get_supabase")
def test_get_goal_404(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.get(f"/learning/goals/{uuid4()}")
    assert r.status_code == 404
    assert "Goal not found" in r.json()["detail"]


@patch("app.routers.learning.get_supabase")
def test_create_goal(mock_get_supabase, client):
    row = _goal_row(title="New Goal")
    mock_table = Mock()
    mock_table.insert.return_value.execute.return_value = Mock(data=[row])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.post("/learning/goals", json={"title": "New Goal", "notes": "n"})
    assert r.status_code == 201
    assert r.json()["title"] == "New Goal"


@patch("app.routers.learning.get_supabase")
def test_update_goal(mock_get_supabase, client):
    goal_id = uuid4()
    row = _goal_row(goal_id=goal_id, title="Updated")
    mock_table = Mock()
    mock_table.update.return_value.eq.return_value.execute.return_value = Mock(data=[row])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.patch(f"/learning/goals/{goal_id}", json={"title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"


@patch("app.routers.learning.get_supabase")
def test_update_goal_404(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.update.return_value.eq.return_value.execute.return_value = Mock(data=[])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.patch(f"/learning/goals/{uuid4()}", json={"title": "x"})
    assert r.status_code == 404


@patch("app.routers.learning.get_supabase")
def test_delete_goal_204(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.delete.return_value.eq.return_value.execute.return_value = Mock(data=None)
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.delete(f"/learning/goals/{uuid4()}")
    assert r.status_code == 204


@patch("app.routers.learning.get_supabase")
def test_delete_goal_404(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.delete.return_value.eq.return_value.execute.return_value = Mock(data=[])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.delete(f"/learning/goals/{uuid4()}")
    assert r.status_code == 404
