from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# DATABASE_URL = "postgresql+psycopg2://user:pass@localhost:5432/mydb"
# для SQLite: "sqlite:///./foo.db"
DATABASE_URL = "sqlite:///foo.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()