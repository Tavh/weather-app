from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import Config

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False} if "sqlite" in Config.SQLALCHEMY_DATABASE_URI else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@contextmanager
def get_session():
    """
    Request-scoped session context manager.
    Handles commit on success, rollback on error, and guaranteed closing.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def init_db():
    """Explicitly create tables."""
    import app.models.user
    import app.models.zone
    print(f"Creating tables in: {Config.SQLALCHEMY_DATABASE_URI}")
    Base.metadata.create_all(bind=engine)
