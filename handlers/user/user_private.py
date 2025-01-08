from aiogram import Router
from dotenv import load_dotenv, find_dotenv

from filters.chat_types import ChatTypeFilter



load_dotenv(find_dotenv())
user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))