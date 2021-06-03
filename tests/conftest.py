import pytest
from emannotationschemas import create_app
import os

@pytest.fixture(scope='session')
def app():
    app = create_app()
    yield app


@pytest.fixture(scope='session')
def client(app):
    client=app.test_client()
    token = os.environ.get('MIDDLE_AUTH_TOKEN', '')
    client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + token
    return client