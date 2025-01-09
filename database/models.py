from sqlalchemy import DateTime, func, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    created = Column(DateTime, default=func.now())  # Дата создания, по умолчанию текущее время
    updated = Column(DateTime, default=func.now(), onupdate=func.now())  # Дата обновления, обновляется при изменении

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    # first_name = Column(String, nullable=True)
    # last_name = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"