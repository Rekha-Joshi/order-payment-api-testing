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