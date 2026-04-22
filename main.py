from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from interfaces.category_interface import (
    add_category,
    get_all_categories,
    remove_category,
    update_category,
)
from interfaces.menu_interface import (
    add_menu_item,
    delete_menu_item,
    get_menu_items,
    update_menu_item,
)
from pydan_schemas.category import (
    GetCategorySchema,
    PostCategorySchema,
    UpdateCategorySchema,
)
from pydan_schemas.menu import (
    GetMenuItemSchema,
    PostMenuItemSchema,
    UpdateMenuItemSchema,
)
from utils.responses import message

app = FastAPI()
env_values = dotenv_values()

# Only accept requests from block95 official website
app.add_middleware(
    CORSMiddleware,
    allow_origins=[(env_values.get("ORIGIN_DOMAIN") or "")],
    allow_methods=["GET"],
    allow_headers=[],
)


# Menu endpoints


@app.get("/")
def root():
    return {"message": "Hello, this is an endpoint for the Block 95 Website"}


@app.get("/menu", response_model=list[GetMenuItemSchema])
def get_menu():
    try:
        menu_items = get_menu_items()
        return menu_items
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to get menu items")


@app.post(
    "/menu",
    status_code=201,
    response_model=GetMenuItemSchema,
)
def add_item(item: PostMenuItemSchema):
    try:
        new_item = add_menu_item(
            name=item.name, price=item.price, oz=item.oz, category_id=item.category_id
        )
        return new_item
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to add item to the menu")


@app.delete("/menu/{item_id}", status_code=204)
def delete_item(item_id: int):
    try:
        deletion_status = delete_menu_item(item_id=item_id)
        if not deletion_status:
            raise HTTPException(status_code=404, detail="Item not found")
        return message(text="Sucessfully deleted item", deleted_item_id=item_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to delete item")


@app.patch("/menu/{item_id}", status_code=200)
def update_item(item: UpdateMenuItemSchema, item_id: int):
    try:
        updated_item = update_menu_item(item=item, item_target_id=item_id)
        if not updated_item:
            raise HTTPException(status_code=404, detail="Item to update not found")
        return message(text="Sucessfully updated item", updated_category=updated_item)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to update item")


# Categories endpoints


# Read all categories
@app.get("/category", status_code=200, response_model=list[GetCategorySchema])
def get_categories():
    try:
        categories = get_all_categories()
        return categories
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to get categories")


# Update categories
@app.patch("/category/{category_id}", status_code=200)
def patch_category(category: UpdateCategorySchema, category_id: int):
    try:
        updated_category = update_category(
            category=category, category_target_id=category_id
        )
        if not updated_category:
            raise HTTPException(
                status_code=404, detail="Cannot find category to update"
            )
        return message(
            text="Sucessfully updated category", updated_category=updated_category
        )

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to update item")


# Delete categories
@app.delete("/category/{category_id}", status_code=204)
def delete_category(category_id: int):
    try:
        deletion_status = remove_category(category_id=category_id)
        if not deletion_status:
            raise HTTPException(
                status_code=404, detail="Category to delete does not exist"
            )
        return message(
            text="Sucessfully deleted_category", deleted_category_id=category_id
        )
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to delete item")


# Create categories
@app.post("/category", response_model=GetCategorySchema, status_code=201)
def post_category(category: PostCategorySchema):
    try:
        new_category = add_category(
            name=category.name,
        )
        return new_category

    except SQLAlchemyError as error:
        if error.__class__ is IntegrityError:
            raise HTTPException(
                status_code=409, detail="Integrity Error: Cannot add duplicate category"
            )
        raise HTTPException(status_code=500, detail="Failed to add category")
