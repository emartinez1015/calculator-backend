import os
import json
import pytest
from chalice import Chalice
from chalice.config import Config
from chalice.local import LocalGateway
from moto import mock_cognitoidp


# Load the config.json file
config_file = '../.chalice/config.json'  # Update with the path to your config file
with open(config_file) as f:
    config_dict = json.load(f)

# Retrieve the environment variables for the 'dev' stage
chalice_stage = os.getenv('AWS_DEFAULT_PROFILE', 'dev')  # Update with your Chalice stage
env_vars = config_dict.get('stages', {}).get(chalice_stage, {}).get('environment_variables', {})

# Set the environment variables for the test execution
os.environ.update(env_vars)

# Import the Chalice app after setting the environment variables
from app import app

app = Chalice(app_name="testclient")

@pytest.fixture(scope='module')
def chalice_client():
    config = Config(config_from_disk=config_dict)
    with mock_cognitoidp():  # Use mock_cognitoidp instead of mock_cognito
        return LocalGateway(app, config=config)


def test_get_operations(chalice_client):
    headers = {'Authorization': 'Allow'}
    response = chalice_client.handle_request(method='GET', path='/v1/operations', headers=headers, body='')

    assert response['statusCode'] == 200
    # Add additional assertions for the expected response

"""
def test_create_record(chalice_client):
    request_data = {
        'operation_id': 1,
        'num1': 5,
        'num2': 10
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Allow'
    }
    response = chalice_client.handle_request(method='POST', path='/v1/records', headers=headers, body=json.dumps(request_data))

    assert response['statusCode'] == 200
    # Add additional assertions for the expected response


def test_random_string(chalice_client, monkeypatch):
    headers = {'Authorization': 'Allow'}
    
    class MockResponse:
        def __init__(self, text, ok=True):
            self.text = text
            self.ok = ok

    def mock_get(*args, **kwargs):
        return MockResponse('string1\nstring2\nstring3\n')

    monkeypatch.setattr('requests.get', mock_get)

    response = chalice_client.handle_request(method='GET', path='/v1/random-string?numeric=true', headers=headers, body='')

    assert response['statusCode'] == 200
    # Add additional assertions for the expected response
"""