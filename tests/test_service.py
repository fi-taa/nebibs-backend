from unittest.mock import Mock, patch
from uuid import uuid4


def _entry_row(entry_id=None, description="Helped at shelter", **kwargs):
    row = {
        "id": str(entry_id or uuid4()),
        "date": "2025-01-15",
        "description": description,
        "hours": 2.0,
        "reflection": "",
        "created_at": "2025-01-01T00:00:00",
        "updated_at": "2025-01-01T00:00:00",
    }
    row.update(kwargs)
    return row


@patch("app.routers.service.get_supabase")
def test_list_entries_empty(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.select.return_value.order.return_value.execute.return_value = Mock(data=[])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.get("/service/entries")
    assert r.status_code == 200
    assert r.json() == []


@patch("app.routers.service.get_supabase")
def test_list_entries_returns_items(mock_get_supabase, client):
    row = _entry_row()
    mock_table = Mock()
    mock_table.select.return_value.order.return_value.execute.return_value = Mock(data=[row])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.get("/service/entries")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["description"] == row["description"]


@patch("app.routers.service.get_supabase")
def test_get_entry_ok(mock_get_supabase, client):
    entry_id = uuid4()
    row = _entry_row(entry_id=entry_id)
    mock_table = Mock()
    mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[row])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.get(f"/service/entries/{entry_id}")
    assert r.status_code == 200
    assert r.json()["id"] == str(entry_id)


@patch("app.routers.service.get_supabase")
def test_get_entry_404(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.select.return_value.eq.return_value.execute.return_value = Mock(data=[])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.get(f"/service/entries/{uuid4()}")
    assert r.status_code == 404
    assert "Entry not found" in r.json()["detail"]


@patch("app.routers.service.get_supabase")
def test_create_entry(mock_get_supabase, client):
    row = _entry_row(description="New entry", hours=3.0)
    mock_table = Mock()
    mock_table.insert.return_value.execute.return_value = Mock(data=[row])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.post(
        "/service/entries",
        json={"date": "2025-02-01", "description": "New entry", "hours": 3.0},
    )
    assert r.status_code == 201
    assert r.json()["description"] == "New entry"
    assert r.json()["hours"] == 3.0


@patch("app.routers.service.get_supabase")
def test_update_entry(mock_get_supabase, client):
    entry_id = uuid4()
    row = _entry_row(entry_id=entry_id, hours=5.0)
    mock_table = Mock()
    mock_table.update.return_value.eq.return_value.execute.return_value = Mock(data=[row])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.patch(f"/service/entries/{entry_id}", json={"hours": 5.0})
    assert r.status_code == 200
    assert r.json()["hours"] == 5.0


@patch("app.routers.service.get_supabase")
def test_delete_entry_204(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.delete.return_value.eq.return_value.execute.return_value = Mock(data=None)
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.delete(f"/service/entries/{uuid4()}")
    assert r.status_code == 204


@patch("app.routers.service.get_supabase")
def test_delete_entry_404(mock_get_supabase, client):
    mock_table = Mock()
    mock_table.delete.return_value.eq.return_value.execute.return_value = Mock(data=[])
    mock_get_supabase.return_value.table.return_value = mock_table

    r = client.delete(f"/service/entries/{uuid4()}")
    assert r.status_code == 404
