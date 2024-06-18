from sqlalchemy.orm import declarative_base

Base = declarative_base()

from shortener.db.models.url import UrlStorage, VIPLink

__all__ = [
    "Base",
    "UrlStorage",
    "VIPLink",
]

