from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product

# Добавление продукта в БД Product
async def add_product_to_db(session: AsyncSession, data: dict):
    try:
        product_name = data['product_name']
        subscription_days = data['subscription_days']
        product_price = data['product_price']
        product_description = data.get('product_description')

        new_product = Product(
            name=product_name,
            count_day=subscription_days,
            price=product_price,
            description=product_description
        )
        session.add(new_product)
        await session.commit()
        print(f"Продукт '{new_product.name}' успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении продукта: {e}")
        await session.rollback()