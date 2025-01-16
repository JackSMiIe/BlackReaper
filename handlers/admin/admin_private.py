from aiogram import Router, types, F
from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from sqlalchemy.ext.asyncio import AsyncSession

from database.product_orm.add_product import add_product_to_db
from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.inline import get_inlineMix_btns
from kbds.reply import get_keyboard, ADMIN_KB

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


# # Обработка команды /admin
@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    await message.answer("Что хотите сделать ⬇️", reply_markup=ADMIN_KB)

# Обработка кнопки '📦 Товары'
@admin_router.message(F.text == '📦 Товары')
async def menu_cmd(message: types.Message):
    await message.answer(
        '<b>Выберите действие:</b>',
        reply_markup=get_inlineMix_btns(btns={
            '🛒 Товары': 'add_product_',  # Добавить товар
            '🎉 Акция': 'add_promotion_',  # Добавить акцию
            '⏳ Пробный период': 'trial_period_',  # Пробный период
            '📊 Ассортимент': 'product_range_',  # Ассортимент
            '🏠 Главное меню': 'main_menu_'  # Главное меню
        }),
        parse_mode='HTML'  # Использование HTML для разметки
    )

""" --- Начало процесса добавления товара --- """
# Определение состояний для процесса добавления товара
class AddProduct(StatesGroup):
    name = State()          # Состояние для ввода названия товара
    count_day = State()     # Состояние для ввода количества дней подписки
    price = State()         # Состояние для ввода цены товара
    description = State()   # Состояние для ввода описания товара

# Обработчик нажатия кнопки 'добавить товар'
@admin_router.callback_query(F.data.startswith('add_product_'))
async def start_adding_product(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название товара:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)  # Переход к состоянию 'name'

# Обработчик для ввода названия товара
@admin_router.message(AddProduct.name, F.text)
async def process_product_name(message: types.Message, state: FSMContext):
    await state.update_data(product_name=message.text)  # Сохраняем введенное название товара
    await message.answer("Введите количество дней подписки:")  # Запрашиваем количество дней
    await state.set_state(AddProduct.count_day)  # Переход к состоянию 'count_day'

# Обработчик для ввода количества дней подписки
@admin_router.message(AddProduct.count_day, F.text)
async def process_subscription_days(message: types.Message, state: FSMContext):
    if not message.text.isdigit():  # Проверка, является ли введенное значение числом
        await message.answer("Введите корректное число для количества дней!")  # Ошибка, если не число
        return
    await state.update_data(subscription_days=int(message.text))  # Сохраняем количество дней
    await message.answer("Введите стоимость товара:")  # Запрашиваем цену товара
    await state.set_state(AddProduct.price)  # Переход к состоянию 'price'

# Обработчик для ввода цены товара
@admin_router.message(AddProduct.price, F.text)
async def process_product_price(message: types.Message, state: FSMContext):
    try:
        price_value = float(message.text)  # Преобразуем введенное значение в число с плавающей точкой
        if price_value < 80:  # Проверка минимальной цены
            await message.answer("Цена должна быть больше 80!")  # Ошибка, если цена меньше 80
            return
    except ValueError:
        await message.answer("Введите корректное число для стоимости!")  # Ошибка, если введено не число
        return

    await state.update_data(product_price=price_value)  # Сохраняем цену товара
    await message.answer("Введите описание товара (или нажмите 'Пропустить'):", reply_markup=get_keyboard('Пропустить', sizes=(1,)))  # Запрашиваем описание товара
    await state.set_state(AddProduct.description)  # Переход к состоянию 'description'

# Обработчик для ввода описания товара
@admin_router.message(AddProduct.description, F.text)
async def process_product_description(message: types.Message, state: FSMContext, session: AsyncSession):
    # Если пользователь ввел "Пропустить", описание товара будет None
    description_text = message.text if message.text.lower() != 'пропустить' else None
    await state.update_data(product_description=description_text)  # Сохраняем описание товара
    data = await state.get_data()  # Получаем все данные, которые были собраны на предыдущих этапах

    try:
        await add_product_to_db(session, data)  # Добавляем товар в базу данных
        # Уведомление об успешном добавлении товара
        await message.answer(
            "Товар успешно добавлен!",
            reply_markup=get_inlineMix_btns(btns={
                'Ассортимент': 'ассортимент_',
                'Назад': 'назад_'
            })
        )
    except Exception as e:
        # Обработка ошибки при добавлении товара
        await message.answer(f"Ошибка при добавлении товара: {e}")
    finally:
        await state.clear()  # Очистка состояния после завершения процесса

"""--- Конец процесса добавления товара ---"""



