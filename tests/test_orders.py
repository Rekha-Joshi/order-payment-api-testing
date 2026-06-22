def test_create_order_success(client, order_data):
    response = client.post(
        "/orders",
        json=order_data["request"]
    )
    assert response.status_code == 201
    
    data = response.json()
    print(data)
    assert "order_id" in data
    assert "customer_id" in data
    assert "status" in data
    assert "total_amount" in data
    assert "items" in data

    assert isinstance(data["order_id"],int)
    assert data["customer_id"] == order_data["request"]["customer_id"]
    assert data["status"] == "pending"

    assert data["total_amount"] == order_data["expected_total"]

def test_get_order_success(client, created_order):
    order_id = created_order["order_id"]
    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200

    data = response.json()
    print(data)
    assert data["order_id"] == created_order["order_id"]
    assert data["customer_id"] == created_order["customer_id"]
    assert data["status"] == "pending"

def test_get_order_not_found(client):
    response = client.get("/orders/999999")

    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert "Order not found" in data["detail"]

def test_create_order_invalid_customer(client, created_product):
    response = client.post(
        "/orders",
        json={
            "customer_id": 9999,
            "items": [
                {
                    "product_id": created_product["id"],
                    "quantity": 2
                }
            ]
        }
    )
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert "customer not found" in data["detail"].lower()

def test_create_order_invalid_product(client, created_customer):
    response = client.post(
        "/orders",
        json={
            "customer_id": created_customer["id"],
            "items": [
                {
                    "product_id": 9999,
                    "quantity": 2
                }
            ]
        }
    )
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()

def test_create_order_insufficient_stock(client,created_customer, created_product):
    response = client.post(
        "/orders",
        json={
            "customer_id": created_customer["id"],
            "items": [
                {
                    "product_id": created_product["id"],
                    "quantity": 99999
                }
            ]
        }
    )
    assert response.status_code == 400

    data = response.json()
    assert "detail" in data
    assert "insufficient stock for product" in data["detail"].lower()

def test_create_order_zero_quantity(client, created_customer, created_product):
    response = client.post(
        "/orders",
        json={
            "customer_id": created_customer["id"],
            "items": [
                {
                    "product_id": created_product["id"],
                    "quantity": 0
                }
            ]
        }
    )
    assert response.status_code == 422

def test_get_customer_orders_success(client, created_order):
    customer_id = created_order["customer_id"]
    response = client.get(f"/customers/{customer_id}/orders")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
    first_order = data[0]
    assert first_order["order_id"] == created_order["order_id"]
    assert first_order["customer_id"] == created_order["customer_id"]
    assert first_order["status"] == "pending"
    assert first_order["total_amount"] == created_order["total_amount"]
