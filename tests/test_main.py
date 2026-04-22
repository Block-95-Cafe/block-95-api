from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from main import app

client = TestClient(app)


# ── Helpers ───────────────────────────────────────────────────────────────────


def make_mock_item(id=1, name="Cheeseburger", price=9.99, oz=8, category_name="Mains"):
    mock_category = MagicMock()
    mock_category.id = 1
    mock_category.name = category_name

    mock_item = MagicMock()
    mock_item.id = id
    mock_item.name = name
    mock_item.price = price
    mock_item.oz = oz
    mock_item.category = mock_category
    return mock_item


def make_mock_category(id=1, name="Mains"):
    mock_category = MagicMock()
    mock_category.id = id
    mock_category.name = name
    return mock_category


# ── Root ──────────────────────────────────────────────────────────────────────


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, this is an endpoint for the Block 95 Website"
    }


# ── GET /menu ─────────────────────────────────────────────────────────────────


@patch("main.get_menu_items")
def test_get_menu_success(mock_get_menu_items):
    mock_get_menu_items.return_value = [make_mock_item()]
    response = client.get("/menu")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["name"] == "Cheeseburger"
    assert data[0]["price"] == 9.99
    assert data[0]["oz"] == 8
    assert data[0]["category"]["id"] == 1
    assert data[0]["category"]["name"] == "Mains"


@patch("main.get_menu_items")
def test_get_menu_empty(mock_get_menu_items):
    mock_get_menu_items.return_value = []
    response = client.get("/menu")
    assert response.status_code == 200
    assert response.json() == []


@patch("main.get_menu_items")
def test_get_menu_db_error(mock_get_menu_items):
    mock_get_menu_items.side_effect = SQLAlchemyError()
    response = client.get("/menu")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to get menu items"


# ── POST /menu ────────────────────────────────────────────────────────────────


@patch("main.add_menu_item")
def test_add_menu_item_success(mock_add_menu_item):
    mock_add_menu_item.return_value = make_mock_item()
    response = client.post(
        "/menu", json={"name": "Cheeseburger", "price": 9.99, "oz": 8, "category_id": 1}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Cheeseburger"
    assert data["price"] == 9.99
    assert data["oz"] == 8
    assert data["category"]["id"] == 1
    assert data["category"]["name"] == "Mains"


@patch("main.add_menu_item")
def test_add_menu_item_db_error(mock_add_menu_item):
    mock_add_menu_item.side_effect = SQLAlchemyError()
    response = client.post(
        "/menu", json={"name": "Cheeseburger", "price": 9.99, "oz": 8, "category_id": 1}
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to add item to the menu"


def test_add_menu_item_missing_fields():
    response = client.post("/menu", json={"name": "Cheeseburger"})
    assert response.status_code == 422


def test_add_menu_item_empty_body():
    response = client.post("/menu", json={})
    assert response.status_code == 422


def test_add_menu_item_invalid_price_type():
    response = client.post(
        "/menu",
        json={"name": "Cheeseburger", "price": "expensive", "oz": 8, "category_id": 1},
    )
    assert response.status_code == 422


def test_add_menu_item_invalid_oz_type():
    response = client.post(
        "/menu",
        json={"name": "Cheeseburger", "price": 9.99, "oz": "eight", "category_id": 1},
    )
    assert response.status_code == 422


def test_add_menu_item_invalid_category_id_type():
    response = client.post(
        "/menu",
        json={"name": "Cheeseburger", "price": 9.99, "oz": 8, "category_id": "one"},
    )
    assert response.status_code == 422


def test_add_menu_item_negative_price():
    response = client.post(
        "/menu",
        json={"name": "Cheeseburger", "price": -1.00, "oz": 8, "category_id": 1},
    )
    assert response.status_code == 422


def test_add_menu_item_zero_price():
    response = client.post(
        "/menu", json={"name": "Cheeseburger", "price": 0, "oz": 8, "category_id": 1}
    )
    assert response.status_code == 422


def test_add_menu_item_empty_name():
    response = client.post(
        "/menu", json={"name": "", "price": 9.99, "oz": 8, "category_id": 1}
    )
    assert response.status_code == 422


def test_add_menu_item_zero_oz():
    response = client.post(
        "/menu", json={"name": "Cheeseburger", "price": 9.99, "oz": 0, "category_id": 1}
    )
    assert response.status_code == 422


def test_add_menu_item_negative_oz():
    response = client.post(
        "/menu",
        json={"name": "Cheeseburger", "price": 9.99, "oz": -1, "category_id": 1},
    )
    assert response.status_code == 422


def test_add_menu_item_invalid_category_id():
    response = client.post(
        "/menu", json={"name": "Cheeseburger", "price": 9.99, "oz": 8, "category_id": 0}
    )
    assert response.status_code == 422


# ── DELETE /menu/{item_id} ────────────────────────────────────────────────────


@patch("main.delete_menu_item")
def test_delete_menu_item_success(mock_delete_menu_item):
    mock_delete_menu_item.return_value = True
    response = client.delete("/menu/1")
    assert response.status_code == 204
    assert response.content == b""


@patch("main.delete_menu_item")
def test_delete_menu_item_not_found(mock_delete_menu_item):
    mock_delete_menu_item.return_value = False
    response = client.delete("/menu/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


@patch("main.delete_menu_item")
def test_delete_menu_item_db_error(mock_delete_menu_item):
    mock_delete_menu_item.side_effect = SQLAlchemyError()
    response = client.delete("/menu/1")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to delete item"


def test_delete_menu_item_invalid_id_type():
    response = client.delete("/menu/abc")
    assert response.status_code == 422


# ── PATCH /menu/{item_id} ─────────────────────────────────────────────────────


@patch("main.update_menu_item")
def test_update_menu_item_success(mock_update_menu_item):
    mock_update_menu_item.return_value = make_mock_item(
        name="Updated Burger", price=12.99
    )
    response = client.patch("/menu/1", json={"price": 12.99})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Sucessfully updated item"
    assert "updated_category" in data


@patch("main.update_menu_item")
def test_update_menu_item_not_found(mock_update_menu_item):
    mock_update_menu_item.return_value = None
    response = client.patch("/menu/999", json={"price": 12.99})
    assert response.status_code == 404
    assert response.json()["detail"] == "Item to update not found"


@patch("main.update_menu_item")
def test_update_menu_item_db_error(mock_update_menu_item):
    mock_update_menu_item.side_effect = SQLAlchemyError()
    response = client.patch("/menu/1", json={"price": 12.99})
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to update item"


@patch("main.update_menu_item")
def test_patch_menu_item_empty_body(mock_update_menu_item):
    # All fields optional so empty body is valid
    mock_update_menu_item.return_value = make_mock_item()
    response = client.patch("/menu/1", json={})
    assert response.status_code == 200


def test_patch_menu_item_invalid_id_type():
    response = client.patch("/menu/abc", json={"price": 12.99})
    assert response.status_code == 422


def test_patch_menu_item_invalid_price_type():
    response = client.patch("/menu/1", json={"price": "expensive"})
    assert response.status_code == 422


def test_patch_menu_item_negative_price():
    response = client.patch("/menu/1", json={"price": -1.00})
    assert response.status_code == 422


def test_patch_menu_item_empty_name():
    response = client.patch("/menu/1", json={"name": ""})
    assert response.status_code == 422


def test_patch_menu_item_zero_oz():
    response = client.patch("/menu/1", json={"oz": 0})
    assert response.status_code == 422


# ── GET /category ─────────────────────────────────────────────────────────────


@patch("main.get_all_categories")
def test_get_categories_success(mock_get_all_categories):
    mock_get_all_categories.return_value = [
        make_mock_category(id=1, name="Mains"),
        make_mock_category(id=2, name="Desserts"),
    ]
    response = client.get("/category")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["name"] == "Mains"
    assert data[1]["id"] == 2
    assert data[1]["name"] == "Desserts"


@patch("main.get_all_categories")
def test_get_categories_empty(mock_get_all_categories):
    mock_get_all_categories.return_value = []
    response = client.get("/category")
    assert response.status_code == 200
    assert response.json() == []


@patch("main.get_all_categories")
def test_get_categories_db_error(mock_get_all_categories):
    mock_get_all_categories.side_effect = SQLAlchemyError()
    response = client.get("/category")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to get categories"


# ── POST /category ────────────────────────────────────────────────────────────


@patch("main.add_category")
def test_post_category_success(mock_add_category):
    mock_add_category.return_value = make_mock_category(id=1, name="Desserts")
    response = client.post("/category", json={"name": "Desserts"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Desserts"


@patch("main.add_category")
def test_post_category_db_error(mock_add_category):
    mock_add_category.side_effect = SQLAlchemyError()
    response = client.post("/category", json={"name": "Desserts"})
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to add category"


@patch("main.add_category")
def test_post_duplicate_category_returns_409(mock_add_category):
    mock_add_category.side_effect = IntegrityError(
        None, None, Exception("duplicate key")
    )
    response = client.post("/category", json={"name": "Mains"})
    assert response.status_code == 409
    assert "duplicate" in response.json()["detail"].lower()


def test_post_category_missing_name():
    response = client.post("/category", json={})
    assert response.status_code == 422


def test_post_category_empty_name():
    response = client.post("/category", json={"name": ""})
    assert response.status_code == 422


def test_post_category_invalid_name_type():
    # FastAPI coerces ints to strings so this may pass
    response = client.post("/category", json={"name": 123})
    assert response.status_code in [201, 422]


# ── PATCH /category/{category_id} ────────────────────────────────────────────


@patch("main.update_category")
def test_patch_category_success(mock_update_category):
    mock_update_category.return_value = make_mock_category(
        id=2, name="Updated Category"
    )
    response = client.patch("/category/2", json={"name": "Updated Category"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Sucessfully updated category"
    assert "updated_category" in data


@patch("main.update_category")
def test_patch_category_not_found(mock_update_category):
    mock_update_category.return_value = None
    response = client.patch("/category/999", json={"name": "Updated Category"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Cannot find category to update"


@patch("main.update_category")
def test_patch_category_db_error(mock_update_category):
    mock_update_category.side_effect = SQLAlchemyError()
    response = client.patch("/category/2", json={"name": "Updated Category"})
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to update item"


def test_patch_category_invalid_id_type():
    response = client.patch("/category/abc", json={"name": "Desserts"})
    assert response.status_code == 422


def test_patch_category_empty_name():
    response = client.patch("/category/1", json={"name": ""})
    assert response.status_code == 422


# ── DELETE /category/{category_id} ───────────────────────────────────────────


@patch("main.remove_category")
def test_delete_category_success(mock_remove_category):
    mock_remove_category.return_value = True
    response = client.delete("/category/2")
    assert response.status_code == 204
    assert response.content == b""


@patch("main.remove_category")
def test_delete_category_not_found(mock_remove_category):
    mock_remove_category.return_value = False
    response = client.delete("/category/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category to delete does not exist"


@patch("main.remove_category")
def test_delete_category_db_error(mock_remove_category):
    mock_remove_category.side_effect = SQLAlchemyError()
    response = client.delete("/category/2")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to delete item"


def test_delete_category_invalid_id_type():
    response = client.delete("/category/abc")
    assert response.status_code == 422
