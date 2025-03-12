import pytest

from {{cookiecutter.project_slug}}.factory import create_app
from {{cookiecutter.project_slug}}.extensions import db


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        yield app  # This ensures the app context is active during tests


@pytest.fixture
def test_client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    """
    Provides a test database session wrapped in an outer transaction.

    This fixture creates all tables and opens a new database connection that starts a single,
    "outer" transaction for the duration of each test. Think of this outer transaction as a
    container that collects every change made during the test. Even if your code calls commit(),
    the changes remain inside this container. At the end of the test, the entire container is
    rolled back, ensuring that no changes persist in the database.
    """
    with app.app_context():
        db.create_all()
        connection = db.engine.connect()
        transaction = connection.begin()

        from sqlalchemy.orm import scoped_session, sessionmaker

        session = scoped_session(sessionmaker(bind=connection))
        db.session = session

        yield session

        transaction.rollback()
        connection.close()
        session.remove()
