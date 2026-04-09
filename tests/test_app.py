from app import app


def test_home_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Portal CI/CD Demo" in response.data


def test_health_route():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_unknown_route():
    client = app.test_client()
    response = client.get("/unknown")
    assert response.status_code == 404


def test_config_exists(monkeypatch):
    monkeypatch.setenv("APP_MODE", "testing")
    client = app.test_client()
    response = client.get("/config")
    assert response.status_code == 200
    assert response.get_json()["app_mode"] == "testing"


def test_config_missing(monkeypatch):
    monkeypatch.delenv("APP_MODE", raising=False)
    client = app.test_client()
    response = client.get("/config")
    assert response.status_code == 500


def test_grade_pass():
    client = app.test_client()
    response = client.post("/grade", json={"score": 80})
    assert response.status_code == 200
    assert response.get_json()["result"] == "pass"


def test_grade_fail():
    client = app.test_client()
    response = client.post("/grade", json={"score": 40})
    assert response.status_code == 200
    assert response.get_json()["result"] == "fail"


def test_grade_missing_score():
    client = app.test_client()
    response = client.post("/grade", json={})
    assert response.status_code == 400


def test_grade_invalid_type():
    client = app.test_client()
    response = client.post("/grade", json={"score": "high"})
    assert response.status_code == 400


def test_grade_out_of_range():
    client = app.test_client()
    response = client.post("/grade", json={"score": 120})
    assert response.status_code == 400