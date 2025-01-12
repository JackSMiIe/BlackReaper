import datetime
from datetime import timedelta
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey, BigInteger, Float, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Модель времени
class Time:
    created = Column(DateTime, default=func.now())  # Дата создания, по умолчанию текущее время
    updated = Column(DateTime, default=func.now(), onupdate=func.now())  # Дата обновления, обновляется при изменении

# Модель для пользователей
class User(Base, Time):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)

    black_list = Column(Boolean, default=False)
    used_trial_product = Column(Boolean, default=False)
    is_vip = Column(Boolean, default=False)  # Поле для клиентов с максимальными привилегиями

    subscriptions = relationship("UserSubscription", back_populates="user")
    purchases = relationship("PurchaseHistory", back_populates="user")

    def __repr__(self):
        return (f"<User(id={self.id}, username={self.username}, email={self.email}, phone_number={self.phone_number}, "
                f"black_list={self.black_list}, used_trial_product={self.used_trial_product}, is_vip={self.is_vip})>")

    def __init__(self, telegram_id, username, email=None, phone_number=None, black_list=False, used_trial_product=False, is_vip=False):
        self.telegram_id = telegram_id
        self.username = username or 'Не указано'
        self.email = email or 'Не указано'
        self.phone_number = phone_number or 'Не указано'
        self.black_list = black_list
        self.used_trial_product = used_trial_product
        self.is_vip = is_vip

# Модель для продуктов (подписок)
class Product(Base, Time):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Название подписки (например, "1 месяц")
    count_day = Column(Integer, nullable=False)  # Количество дней подписки
    price = Column(Integer, nullable=False)  # Цена подписки (в копейках)
    description = Column(String, nullable=True)  # Описание продукта (необязательное поле)

    # Здесь добавляем relationship
    subscriptions = relationship("UserSubscription", back_populates="product",passive_deletes=True)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, count_day={self.count_day}, price={self.price / 100:.2f}, description={self.description})>"

    def __init__(self, name, count_day, price, description=None):
        self.name = name
        self.count_day = count_day
        self.price = int(round(price * 100))  # Переводим цену в копейки
        self.description = description

# Модель для подписок пользователей
class UserSubscription(Base):
    __tablename__ = 'user_subscriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)  # Индекс на user_id
    product_id = Column(Integer, ForeignKey('products.id', ondelete='SET NULL'), nullable=True, index=True)  # Индекс на product_id
    quantity = Column(Integer, default=1)
    start_date = Column(Date, nullable=False, default=func.now())
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="subscriptions")
    product = relationship("Product", back_populates="subscriptions")

    # Добавляем два индекса:
    # 1. Индекс на user_id и product_id
    # 2. Комбинированный индекс на user_id, product_id и is_active
    __table_args__ = (
        Index('ix_user_product', 'user_id', 'product_id'),  # Индекс на пару user_id + product_id
        Index('ix_user_product_active', 'user_id', 'product_id', 'is_active')  # Индекс на user_id + product_id + is_active
    )

    def __repr__(self):
        return f"<UserSubscription(user_id={self.user_id}, product_id={self.product_id}, is_active={self.is_active})>"

    def __init__(self, user_id, product_id, quantity=1, is_active=True, product=None):
        if not product:
            raise ValueError("Product must be provided if no product_id is set.")
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.is_active = is_active

        # Если передан продукт, рассчитываем конечную дату
        if product:
            self.product = product
            self.end_date = self.start_date + timedelta(days=product.count_day)
        else:
            self.end_date = None
""" Запросы с использованием индексов:
1. Поиск всех активных подписок для конкретного пользователя:
    active_subscriptions = session.query(Product).join(UserSubscription).filter(
    UserSubscription.user_id == user_id,
    UserSubscription.is_active == True
).all()
"""
class PurchaseHistory(Base):
    __tablename__ = 'purchase_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    month_year = Column(String, nullable=False)  # Месяц и год покупки

    user = relationship("User", back_populates="purchases")

    def __repr__(self):
        return f"<PurchaseHistory(user_id={self.user_id}, amount={self.amount}, month_year={self.month_year})>"

    def __init__(self, user_id, amount):
        self.user_id = user_id
        self.amount = amount
        self.month_year = datetime.now().strftime('%Y-%m')  # Формируем месяц и год в нужном формате