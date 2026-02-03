from typing import Generator, Any

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@172.17.0.2:5432/app"
# для SQLite: "sqlite:///./foo.db"
# DATABASE_URL = "sqlite:///foo.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

constraint_naming_conventions = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=constraint_naming_conventions)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db() -> Generator[Session, Any, None]:
    database_session = SessionLocal()
    try:
        yield database_session
        database_session.commit()
    except Exception:
        database_session.rollback()
        raise
    finally:
        database_session.close()