import pytest
from app import create_app, db as _db


@pytest.fixture(scope="session")
def app():
    # "testing" config must be chosen at creation time: Flask-SQLAlchemy binds the
    # engine inside init_app(), so overriding the URI afterwards has no effect and
    # the tests would run (and drop_all) against the development database.
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_headers(client):
    """Register a test user and return JWT headers."""
    client.post("/api/auth/register", json={
        "name": "Teste User",
        "email": "teste@medilembre.com",
        "password": "senha123",
    })
    resp = client.post("/api/auth/login", json={
        "email": "teste@medilembre.com",
        "password": "senha123",
    })
    token = resp.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}
