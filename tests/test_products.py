def test_create_product_success(client, product_data):
    response = client.post(
        "/products",
        json=product_data
    )
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]
    assert data["stock"] == product_data["stock"]

def test_get_product_success(client, created_product):
    product_id = created_product["id"]
    response = client.get(
        f"/products/{product_id}"
    )
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == created_product["id"]
    assert data["name"] == created_product["name"]
    assert data["price"] == created_product["price"]
    assert data["stock"] == created_product["stock"]

def test_get_product_not_found(client):
    response = client.get("/products/999999")
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()