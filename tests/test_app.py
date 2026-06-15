from fastapi.testclient import TestClient

from main import app, store


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["app"] == "PROMPTER"


def test_enhance() -> None:
    response = client.post(
        "/api/enhance",
        json={
            "prompt": "Summarize our release notes.",
            "goal": "Improve structure",
            "audience": "General LLM",
            "constraints": ["Use bullets"],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert "enhanced" in payload
    assert payload["metrics"]["overall"] > 0


def test_versions_roundtrip() -> None:
    create = client.post(
        "/api/versions",
        json={
            "title": "Release summary prompt",
            "prompt": "Write a release summary.",
            "notes": "First saved version",
            "tags": ["release", "summary"],
        },
    )
    assert create.status_code == 200
    item = create.json()

    listed = client.get("/api/versions")
    assert listed.status_code == 200
    versions = listed.json()["versions"]
    assert any(version["id"] == item["id"] for version in versions)


def test_settings() -> None:
    response = client.get("/api/settings")
    assert response.status_code == 200
    payload = response.json()
    assert payload["app_name"] == "PROMPTER"
    assert "data_dir" in payload


def test_store_file_exists() -> None:
    store.load()
    assert store.path.parent.exists()
