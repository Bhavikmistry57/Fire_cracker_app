import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from app.models import Base
from app.seed import seed_products

load_dotenv()

DATABASE_PATH = os.environ.get("DATABASE_PATH", "./data/shop.db")


def _sqlite_url(path: str) -> str:
    resolved = Path(path).expanduser()
    if not resolved.is_absolute():
        resolved = Path.cwd() / resolved
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{resolved}"


engine = create_engine(
    _sqlite_url(DATABASE_PATH),
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    if "image_url" not in {column["name"] for column in inspect(engine).get_columns("products")}:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE products ADD COLUMN image_url VARCHAR(500)"))
    db = SessionLocal()
    try:
        seed_products(db)
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
