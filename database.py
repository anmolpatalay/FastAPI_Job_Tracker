import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

db_driver = os.getenv("DB_DRIVER", "mysql+pymysql")
db_host = os.getenv("DB_HOST", "localhost")
on_render = os.getenv("RENDER", "").lower() == "true"
use_sqlite = db_driver.startswith("sqlite") or (
    on_render and db_host in ("", "localhost", "127.0.0.1")
)

if use_sqlite:
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./job_tracker.db")
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
else:
    SQLALCHEMY_DATABASE_URL = URL.create(
        drivername=db_driver,
        username=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        host=db_host,
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "job_tracker"),
    )
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BASE = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
