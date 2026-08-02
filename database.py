import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername=os.getenv('DB_DRIVER', 'mysql+pymysql'),
    username=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', '3306')),
    database=os.getenv('DB_NAME', 'job_tracker'),
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