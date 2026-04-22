from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker


def make_engine():
    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username="jordidiaz",
        password="",
        host="localhost",
        port=5432,
        database="block95",
    )
    return create_engine(db_url, echo=True)


database_engine = make_engine()
Session = sessionmaker(bind=database_engine)
