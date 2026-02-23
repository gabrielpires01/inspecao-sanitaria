import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.core.database import Base, get_db
from app.main import app
from app.models.user import User
from app.core.security import get_password_hash
from faker import Faker

fake = Faker("pt_BR")

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    return {
        "email": fake.email(),
        "password": "Teste123!@#",
        "full_name": fake.name(),
        "username": fake.user_name()
    }


@pytest.fixture
def sample_user(db_session, sample_user_data):
    user = User(
        email=sample_user_data["email"],
        hashed_password=get_password_hash(sample_user_data["password"]),
        full_name=sample_user_data["full_name"],
        username=sample_user_data["username"]
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, sample_user, sample_user_data):
    response = client.post(
        "/api/auth/login",
        data={
            "username": sample_user_data["username"],
            "password": sample_user_data["password"]
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_establishment_data():
    return {
        "name": fake.company(),
        "address": fake.address(),
        "cep": fake.postcode(),
        "city": fake.city()
    }


@pytest.fixture
def sample_establishment(db_session, sample_establishment_data):
    from app.models.inspection import Establishments
    establishment = Establishments(**sample_establishment_data)
    db_session.add(establishment)
    db_session.commit()
    db_session.refresh(establishment)
    return establishment


@pytest.fixture
def sample_inspection_data(sample_establishment):
    from app.enums import Status
    return {
        "establishment_id": sample_establishment.id,
        "status": Status.clear
    }


@pytest.fixture
def sample_inspection(db_session, sample_establishment, sample_user):
    from app.models.inspection import Inspections
    from app.enums import Status
    inspection = Inspections(
        establishment_id=sample_establishment.id,
        inspector_id=sample_user.id,
        status=Status.clear
    )
    db_session.add(inspection)
    db_session.commit()
    db_session.refresh(inspection)
    return inspection


@pytest.fixture
def sample_finalized_inspection(db_session, sample_establishment, sample_user):
    from app.models.inspection import Inspections
    from app.models.irregularity import Irregularities
    from app.enums import Status, Severity
    inspection = Inspections(
        establishment_id=sample_establishment.id,
        inspector_id=sample_user.id,
        status=Status.has_irregularities
    )
    db_session.add(inspection)
    db_session.commit()
    db_session.refresh(inspection)

    irregularity = Irregularities(
        inspection_id=inspection.id,
        inspector_id=sample_user.id,
        severity=Severity.major,
        description="Irregularidade para finalizar"
    )

    db_session.add(irregularity)
    db_session.commit()
    db_session.refresh(irregularity)

    inspection.status = Status.finalized
    db_session.commit()
    db_session.refresh(inspection)

    return irregularity


@pytest.fixture
def sample_irregularity(db_session, sample_inspection, sample_user):
    from app.models.irregularity import Irregularities
    from app.enums import Severity
    irregularity = Irregularities(
        inspection_id=sample_inspection.id,
        inspector_id=sample_user.id,
        severity=Severity.major
    )
    db_session.add(irregularity)
    db_session.commit()
    db_session.refresh(irregularity)
    return irregularity