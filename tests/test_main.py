def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["service"] == "nebibs-backend"
    assert data["docs"] == "/docs"


def test_docs_ui(client):
    r = client.get("/docs")
    assert r.status_code == 200


def test_openapi_json(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    schema = r.json()
    assert "openapi" in schema
    assert "paths" in schema
