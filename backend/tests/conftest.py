import pytest
from backend.app.extensions import db
from app import create_app
import os



@pytest.fixture(scope='module')
def test_client():
    os.environ['CONFIG_TYPE'] = 'TestConfig'
    my_app = create_app()
    with my_app.test_client() as testing_client:
        with my_app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def init_database():
    db.create_all()
    yield
    db.drop_all()
