from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL


SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="Ramanujan@2003",
    host="localhost",
    port=3306,
    database="job_tracker",
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit = False, autoflush=False,bind=engine)

BASE = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()