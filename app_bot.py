import asyncio
from bot_instance import bot
from aiogram import Dispatcher, types

from common.bot_cmds_list import private
from middlewares.db import DataBaseSession
from database.engine import create_db, drop_db, session_maker
from handlers.user.user_private import user_private_router
from handlers.admin.admin_private import admin_router


#ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']

# bot.my_admins_list = [int(os.getenv('ADMIN_LIST'))]

# Получение строки с администраторами из переменной окружения

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(admin_router)

async def on_startup(bot):  # dp передается автоматически при старте
    run_param = True
    if run_param:
        await drop_db()
    await create_db()
    # asyncio.create_task(check_subscriptions(session_maker()))
    # asyncio.create_task(check_blacklisted_users(session_maker()))
    # asyncio.create_task(check_subscriptions_trial(session_maker()))

async def on_shutdown(bot):
    print('Bot ERROR')



async def main():
    #await create_db() # Создаст все бд
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)

    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



asyncio.run(main())