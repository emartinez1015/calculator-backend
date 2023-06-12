import os
import json
import pytest
from chalice.config import Config
from chalice.local import LocalGateway
from moto import mock_cognitoidp


config_file = '../.chalice/config.json'
with open(config_file) as f:
    config_dict = json.load(f)

chalice_stage = os.getenv('AWS_DEFAULT_PROFILE', 'dev')
env_vars = config_dict.get('stages', {}).get(chalice_stage, {}).get('environment_variables', {})

os.environ.update(env_vars)

from app import app

@pytest.fixture(scope='module')
def auth_token(chalice_client):
    request_data = {
        'username': 'test@test.com',
        'password': 'Cx52020..'
    }
    headers = {'Content-Type': 'application/json'}
    response = chalice_client.handle_request(method='POST', path='/v1/signin', headers=headers, body=json.dumps(request_data))
    data = json.loads(response['body'])
    return data['access_token']


@pytest.fixture(scope='module')
def chalice_client():
    config = Config(config_from_disk=config_dict)
    with mock_cognitoidp():
        return LocalGateway(app, config=config)


def test_get_operations(chalice_client, auth_token):
    headers = {'Authorization': auth_token}
    response = chalice_client.handle_request(method='GET', path='/v1/operations', headers=headers, body='')
    assert response['statusCode'] == 200


def test_create_record(chalice_client, auth_token):
    request_data = {
        'operation_id': 1,
        'num1': "5",
        'num2': "10"
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_token
    }
    response = chalice_client.handle_request(method='POST', path='/v1/records', headers=headers, body=json.dumps(request_data))

    assert response['statusCode'] == 200


def test_random_string(chalice_client, monkeypatch, auth_token):
    headers = {'Authorization': auth_token}
    class MockResponse:
        def __init__(self, text, ok=True):
            self.text = text
            self.ok = ok

    def mock_get(*args, **kwargs):
        return MockResponse('string1\nstring2\nstring3\n')

    monkeypatch.setattr('requests.get', mock_get)

    response = chalice_client.handle_request(method='GET', path='/v1/random-string?numeric=true', headers=headers, body='')

    assert response['statusCode'] == 200
