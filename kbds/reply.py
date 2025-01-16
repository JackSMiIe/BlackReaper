from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int, ...] = (2,),
        additional_buttons: list = None  # Добавляем параметр для дополнительных кнопок
):
    if additional_buttons is None:
        additional_buttons = []  # Если не переданы дополнительные кнопки, создаем пустой список

    keyboard = ReplyKeyboardBuilder()

    # Добавляем обычные кнопки
    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    # Добавляем дополнительные кнопки, если они есть
    for button in additional_buttons:
        keyboard.add(KeyboardButton(text=button))

    # Возвращаем клавиатуру с нужными размерами
    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)

# Клавиатура Администратора
ADMIN_KB = get_keyboard(
    "📦 Товары",
    "🚫 ЧС",
    "👤 Пользователи",
    "📊 Статистика",
    "🔑 Администраторы",
    "🛠 Техподдержка",
    placeholder="Выберите действие 👇",
    sizes=(3, 3),
)

