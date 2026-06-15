import pytest
from fastapi.testclient import TestClient
from faker import Faker

from app.main import app

fake = Faker()

@pytest.fixture
def customer_data():
    first_name = fake.first_name()
    last_name = fake.last_name()

    return {
        "name": f"{first_name} {last_name}",
        "email": f"{first_name.lower()}.{last_name.lower()}@orderpay.com"
    }

@pytest.fixture
def client():
    return TestClient(app) # This creates our resulable FastAPI test client