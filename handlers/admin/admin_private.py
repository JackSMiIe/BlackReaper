from aiogram import Router, types
from aiogram.filters import CommandStart

from filters.chat_types import ChatTypeFilter, IsAdmin
from handlers.user.user_private import user_private_router

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())



@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Hello')