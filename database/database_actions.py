from database.db_schema import Base, Category, MenuItem
from database.engine import database_engine


def generate_schema():
    print("Creating tables from schema...")
    Base.metadata.create_all(database_engine)
