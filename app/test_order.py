from fastapi.testclient import TestClient
from process_orders import app
import math

client = TestClient(app)


def test_process_orders_complete():
    response = client.post(
        "/solution",
        json={
            "orders": [
                {
                    "id": 1,
                    "item": "Laptop",
                    "quantity": 1,
                    "price": 999.99,
                    "status": "completed",
                },
                {
                    "id": 2,
                    "item": "Smartphone",
                    "quantity": 2,
                    "price": 499.95,
                    "status": "pending",
                },
                {
                    "id": 3,
                    "item": "Headphones",
                    "quantity": 3,
                    "price": 99.90,
                    "status": "completed",
                },
                {
                    "id": 4,
                    "item": "Mouse",
                    "quantity": 4,
                    "price": 24.99,
                    "status": "canceled",
                },
            ],
            "criterion": "completed",
        },
    )
    assert response.status_code == 200
    assert math.isclose(response.json(),1299.69)


def test_negative_price():
    response = client.post(
        "/solution",
        json={
            "orders": [
                {
                    "id": 1,
                    "item": "Laptop",
                    "quantity": 1,
                    "price": -999.99,
                    "status": "completed",
                },
                {
                    "id": 2,
                    "item": "Smartphone",
                    "quantity": 2,
                    "price": 499.95,
                    "status": "pending",
                },
                {
                    "id": 3,
                    "item": "Headphones",
                    "quantity": 3,
                    "price": 99.90,
                    "status": "completed",
                },
                {
                    "id": 4,
                    "item": "Mouse",
                    "quantity": 4,
                    "price": 24.99,
                    "status": "canceled",
                },
            ],
            "criterion": "completed",
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "greater_than_equal",
                "loc": ["body", "orders", 0, "price"],
                "msg": "Input should be greater than or equal to 0",
                "input": -999.99,
                "ctx": {"ge": 0},
                "url": "https://errors.pydantic.dev/2.4/v/greater_than_equal",
            }
        ]
    }


def test_order_status():
    response = client.post(
        "/solution",
        json={
            "orders": [
                {
                    "id": 1,
                    "item": "Laptop",
                    "quantity": 1,
                    "price": 999.99,
                    "status": "completed",
                },
                {
                    "id": 2,
                    "item": "Smartphone",
                    "quantity": 2,
                    "price": 499.95,
                    "status": "pending",
                },
                {
                    "id": 3,
                    "item": "Headphones",
                    "quantity": 3,
                    "price": 99.90,
                    "status": "completed",
                },
                {
                    "id": 4,
                    "item": "Mouse",
                    "quantity": 4,
                    "price": 24.99,
                    "status": "canceled",
                },
            ],
            "criterion": "invalid",
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "enum",
                "loc": ["body", "criterion"],
                "msg": "Input should be 'completed', 'pending', 'canceled' or 'all'",
                "input": "invalid",
                "ctx": {"expected": "'completed', 'pending', 'canceled' or 'all'"},
            }
        ]
    }


def test_order_status_all():
    response = client.post(
        "/solution",
        json={
            "orders": [
                {
                    "id": 1,
                    "item": "Laptop",
                    "quantity": 1,
                    "price": 999.99,
                    "status": "completed",
                },
                {
                    "id": 2,
                    "item": "Smartphone",
                    "quantity": 2,
                    "price": 499.95,
                    "status": "pending",
                },
                {
                    "id": 4,
                    "item": "Mouse",
                    "quantity": 4,
                    "price": 24.99,
                    "status": "canceled",
                },
            ],
            "criterion": "all",
        },
    )
    assert response.status_code == 200
    assert math.isclose(response.json(),2099.85)

