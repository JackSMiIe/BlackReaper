from sqlalchemy import DateTime, func, Column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    created = Column(DateTime, default=func.now())  # Дата создания, по умолчанию текущее время
    updated = Column(DateTime, default=func.now(), onupdate=func.now())  # Дата обновления, обновляется при изменении


