import pytest
from tinifyUrl import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def client(app):
    return app.test_client()
