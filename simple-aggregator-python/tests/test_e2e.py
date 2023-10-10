from unittest.mock import Mock, MagicMock

import pytest
from dependency_injector import providers
from fastapi import FastAPI
from fastapi.testclient import TestClient
from simple_aggregator_python.app import app

@pytest.fixture(scope='session')
def client():
    d = {
        'table_name': 'events3',
        'data_path': 'data/*.csv'
    }
    app.container.config.from_dict(d)
    client = TestClient(app)
    yield client


def test_get_with_customer_id(client):
    response = client.get('/events/b4f9279a0196e40632e947dd1a88e857?start_timestamp=2021-03-01%2000:00:00&end_timestamp=2021-03-01%2010:00:00')
    assert response.status_code == 200
    assert len(response.json()["data"]) == 10
    assert response.json()["customer_id"] == 'b4f9279a0196e40632e947dd1a88e857'


def test_bad_request_with_no_path_paramn(client):
    response = client.get('/events/?start_timestamp=2021-03-01%2000:00:00&end_timestamp=2021-03-01%2010:00:00')
    assert response.status_code == 404


def test_bad_request_with_no_time_params(client):
    response = client.get('/events/b4f9279a0196e40632e947dd1a88e857')
    assert response.status_code == 422
