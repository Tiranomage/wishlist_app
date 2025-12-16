from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import get_settings


settings = get_settings()


class Base(DeclarativeBase):
	pass


# Для SQLite нужно использовать другие параметры
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20,
        echo=False,
        future=True,
        connect_args={"check_same_thread": False}  # Для SQLite
    )
else:
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20,
        echo=False,
        future=True
    )
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Generator:
	db = SessionLocal()
	try:
		yield db
	except Exception as e:
		db.rollback()
		raise e
	finally:
		try:
			db.close()
		except Exception:
			# Ignore errors during closing the session
			pass


