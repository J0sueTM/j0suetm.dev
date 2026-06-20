from http import HTTPStatus

from starlette.testclient import TestClient

from j0suetm.entrypoints.cli import start_app


def test_get_health() -> None:
    response = TestClient(start_app()).get("/api/health")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "healthy"}
