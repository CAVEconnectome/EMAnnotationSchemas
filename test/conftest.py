import pytest
from emannotationschemas import create_app

@pytest.fixture(scope='session')
def app():
    app = create_app()
    yield app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()
