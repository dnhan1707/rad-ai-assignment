import pytest
from src.main import create_application
from fastapi.testclient import TestClient

@pytest.fixture(scope='session')
def testing_app():
    app = create_application()
    testing_app = TestClient(app)
    return testing_app
