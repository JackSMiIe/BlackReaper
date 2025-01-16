from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from filters.chat_types import ChatTypeFilter
from kbds.reply import get_keyboard

load_dotenv(find_dotenv())


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


# Команда старт
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    """Проверяем, находится ли пользователь в черном списке"""

    # Если пользователь не в черном списке, продолжаем выполнение
    await state.clear()
    user = message.from_user.first_name or message.from_user.username or "Уважаемый пользователь"
    await message.answer(
        f"Здравствуйте, <b>{user}</b>! 👋\n\n"
        f"Добро пожаловать в наш бот. 🌐 Мы предоставляем доступ к защищённой сети, которая обеспечивает стабильность и "
        f"безопасность при работе в интернете, благодаря нашим серверам, расположенным в Нидерландах 🇳🇱.\n\n"
        f"Пользуйтесь сетью без лишних забот — ваша конфиденциальность и защита данных в надежных руках. 🔒✨\n\n"
        f"Если у вас возникнут вопросы или понадобится помощь, мы всегда готовы помочь! 😊\n\n"
        f"Выберите действие 👇",
        parse_mode='HTML',
        reply_markup=get_keyboard(
            "💼 Тарифы",
            "🎁 Пробный период",
            "👤 Личный кабинет",
            "📖 Инструкции",
            "🛠 Поддержка",
            placeholder="Что вас интересует?",
            sizes=(2, 2, 1),
        ),
    )

