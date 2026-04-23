from sqlalchemy import select

from database.db_schema import Category, MenuItem
from database.engine import Session
from pydan_schemas.menu import UpdateMenuItemSchema


def get_menu_items():
    """
    Gets all the items within the menu table along with categories
    """
    with Session() as db:
        menu_items = db.execute(select(Category)).scalars().all()
        return menu_items


def add_menu_item(name: str, price: float, oz: int, category_id: int):
    """
    Adds a single item to the menu table
    """
    item = MenuItem(name=name, price=price, oz=oz, category_id=category_id)
    with Session() as db:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item


def delete_menu_item(item_id: int):
    """
    Deletes a single item from the menu table
    """
    with Session() as db:
        item = db.get(MenuItem, item_id)
        if item:
            db.delete(item)
            db.commit()
            return True
        return False


def update_menu_item(item: UpdateMenuItemSchema, item_target_id: int):
    """
    Updates a single menu item
    """
    with Session() as db:
        target_item = db.get(MenuItem, item_target_id)
        if target_item:
            for key, value in item:
                if value is not None:
                    setattr(target_item, key, value)
            db.commit()
            db.refresh(target_item)
            return target_item
    return None
