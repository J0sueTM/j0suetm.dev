from http import HTTPStatus

from starlette.testclient import TestClient

from j0suetm.infra.app import app


def test_get_health() -> None:
    client = TestClient(app)

    response = client.get("/api/health")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "healthy"}
