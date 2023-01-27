import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tgbot.config import Config

from tgbot.handlers.admin import admin_router
from tgbot.handlers.echo import echo_router
from tgbot.handlers.user import user_router
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.services import broadcaster

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот был запущен")


def register_global_middlewares(dp: Dispatcher, config):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    storage = MemoryStorage()
    bot = Bot(token=Config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    await bot.delete_webhook(drop_pending_updates=True)

    for router in [
        admin_router,
        user_router,
        echo_router
    ]:
        dp.include_router(router)

    register_global_middlewares(dp, Config)

    await on_startup(bot, Config.bot_admins)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот был выключен!")
