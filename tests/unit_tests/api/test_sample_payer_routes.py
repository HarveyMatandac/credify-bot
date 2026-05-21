import json
import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from payer_website_autofiller.frontend.main import app

DEPLOYMENT_FUNCTION = (
    "payer_website_autofiller.frontend.routers.sample_payer.run_deployment"
)
ROUTE = "/api/bots/sample_payer/sample_website/"


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def load_json():
    file_path = (
        "/home/ianharveymatandac/workspace/training"
        + "/payer-website-autofiller/tests/inputs/template.json"
    )
    with open(file_path) as f:
        return json.load(f)


@pytest.fixture
def mock_run_deployment(mocker):
    yield mocker.patch(
        DEPLOYMENT_FUNCTION,
        return_value=None,
    )


def test_sample_website_route(mock_run_deployment, client, load_json):
    response = client.post(ROUTE, json=load_json)

    print(response.json())

    assert response.status_code == 200


def test_sample_website_generic_error(mocker, client, load_json):
    mocker.patch(DEPLOYMENT_FUNCTION, side_effect=Exception("Error"))

    response = client.post(ROUTE, json=load_json)

    assert response.status_code == 500
