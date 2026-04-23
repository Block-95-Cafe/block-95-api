from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from config import settings


def make_engine():
    db_url = settings.database_url
    return create_engine(db_url, echo=True)


database_engine = make_engine()
Session = sessionmaker(bind=database_engine)
