from sqlalchemy import select

from database.db_schema import Category
from database.engine import Session
from pydan_schemas.category import UpdateCategorySchema


def get_all_categories():
    """
    Gets all the categories within the categories table.
    """
    with Session() as db:
        categories = db.execute(select(Category)).scalars().all()
        return categories


def add_category(name: str):
    """
    Adds a category to the categories table
    """
    item = Category(name=name)
    with Session() as db:
        db.add(item)
        db.commit()
        db.refresh(item)
        return item


def remove_category(category_id: int):
    """
    Deletes a single category from the category table
    """
    with Session() as db:
        item = db.get(Category, category_id)
        if item:
            db.delete(item)
            db.commit()
            return True
        return False


def update_category(category: UpdateCategorySchema, category_target_id: int):
    """
    Updates a single category
    """
    with Session() as db:
        target_item = db.get(Category, category_target_id)
        if target_item:
            for key, value in category:
                if value is not None:
                    setattr(target_item, key, value)
            db.commit()
            db.refresh(target_item)
            return target_item
        return None
