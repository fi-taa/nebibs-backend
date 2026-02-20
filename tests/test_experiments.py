from unittest.mock import Mock, patch
from uuid import uuid4


def _experiment_row(experiment_id=None, title="Exp 1", **kwargs):
    row = {
        "id": str(experiment_id or uuid4()),
        "title": title,
        "description": "",
        "dependencies": [],
        "next_action": "",
        "status": "not_started",
        "notes": "",
        "created_at": "2025-01-01T00:00:00",
        "updated_at": "2025-01-01T00:00:00",
    }
    row.update(kwargs)
    return row


@patch("app.routers.experiments.get_supabase")
def test_list_experiments_empty(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.select.return_value.order.return_value.execute.return_value = Mock(data=[])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.get("/experiments")
    assert r.status_code == 200
    assert r.json() == []


@patch("app.routers.experiments.get_supabase")
def test_list_experiments_returns_items(mock_get_supabase, client):
    row = _experiment_row()
    mock_table = Mock()
    mock_table.select.return_value.order.return_value.execute.return_value = Mock(data=[row])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.get("/experiments")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["title"] == row["title"]


@patch("app.routers.experiments.get_supabase")
def test_get_experiment_ok(mock_get_supabase, client):
    experiment_id = uuid4()
    row = _experiment_row(experiment_id=experiment_id)
    mock_table = Mock()
    mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[row])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.get(f"/experiments/{experiment_id}")
    assert r.status_code == 200
    assert r.json()["id"] == str(experiment_id)


@patch("app.routers.experiments.get_supabase")
def test_get_experiment_404(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.get(f"/experiments/{uuid4()}")
    assert r.status_code == 404
    assert "Experiment not found" in r.json()["detail"]


@patch("app.routers.experiments.get_supabase")
def test_create_experiment(mock_get_supabase, client):
    row = _experiment_row(title="New Exp")
    mock_table = Mock()
    mock_table.insert.return_value.execute.return_value = Mock(data=[row])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.post(
        "/experiments",
        json={"title": "New Exp", "description": "d", "status": "in_progress"},
    )
    assert r.status_code == 201
    assert r.json()["title"] == "New Exp"


@patch("app.routers.experiments.get_supabase")
def test_update_experiment(mock_get_supabase, client):
    experiment_id = uuid4()
    row = _experiment_row(experiment_id=experiment_id, status="completed")
    mock_table = Mock()
    mock_table.update.return_value.eq.return_value.execute.return_value = Mock(data=[row])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.patch(f"/experiments/{experiment_id}", json={"status": "completed"})
    assert r.status_code == 200
    assert r.json()["status"] == "completed"


@patch("app.routers.experiments.get_supabase")
def test_delete_experiment_204(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.delete.return_value.eq.return_value.execute.return_value = Mock(data=None)
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.delete(f"/experiments/{uuid4()}")
    assert r.status_code == 204


@patch("app.routers.experiments.get_supabase")
def test_delete_experiment_404(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.delete.return_value.eq.return_value.execute.return_value = Mock(data=[])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.delete(f"/experiments/{uuid4()}")
    assert r.status_code == 404
