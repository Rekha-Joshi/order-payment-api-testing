def test_create_customer_success(client, customer_data):
    response = client.post(
        "/customers", 
        json=customer_data
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == customer_data["name"]
    assert data["email"] == customer_data["email"]
    assert "id" in data
    assert isinstance(data["id"], int)

def test_create_customer_duplicate_email(client, customer_data):
    response1 = client.post(
        "/customers",
        json=customer_data
    )

    response2 = client.post(
        "/customers",
        json=customer_data
    )
    assert response1.status_code == 201
    assert response2.status_code == 409

def test_get_customer_success(client, created_customer):
    customer_id = created_customer["id"]

    response = client.get(
        f"/customers/{customer_id}"
    )
    assert response.status_code == 200 #customer is fetched successfully

    data = response.json()

    assert "id" in data
    assert "name" in data
    assert "email" in data

    assert data["id"] == customer_id
    assert data["name"] == created_customer["name"]
    assert data["email"] == created_customer["email"]

def test_get_customer_not_found(client):
    response = client.get("/customers/99999")

    assert response.status_code == 404
    data = response.json()

    assert "detail" in data
    assert "not found" in data["detail"].lower()

def test_get_customer_orders_no_orders(client, created_customer):
    customer_id = created_customer["id"]
    response = client.get(f"/customers/{customer_id}/orders")

    assert response.status_code == 200

    data = response.json()
    assert "detail" in data
    assert "No orders" in data["detail"]
    