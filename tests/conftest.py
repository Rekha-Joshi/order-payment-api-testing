import pytest
from fastapi.testclient import TestClient
from faker import Faker

from app.main import app

fake = Faker()

@pytest.fixture
def client():
    return TestClient(app) # This creates our resulable FastAPI test client

@pytest.fixture
def customer_data():
    first_name = fake.first_name()
    last_name = fake.last_name()

    return {
        "name": f"{first_name} {last_name}",
        "email": f"{first_name.lower()}.{last_name.lower()}@orderpay.com"
    }

@pytest.fixture
def created_customer(client, customer_data):
    response = client.post(
        "/customers",
        json=customer_data
    )
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def product_data():
    name = f"{fake.word().title()} Product"
    return {
        "name": name,
        "price": round(fake.random.uniform(10,500),2),
        "stock": fake.random_int(min=3, max=10)
    }

@pytest.fixture
def created_product(client, product_data):
    response = client.post(
        "/products",
        json=product_data
    )
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def order_data(created_customer, created_product):
    quantity = 2
    return{
        "request": {
            "customer_id":created_customer["id"],
            "items":[
                {
                    "product_id":created_product["id"],
                    "quantity":2
                }
            ]
        },
        "expected_total":created_product["price"] * quantity
    }

@pytest.fixture
def created_order(client, order_data):
    response = client.post(
        "/orders",
        json=order_data["request"]
    )
    assert response.status_code == 201
    return response.json()