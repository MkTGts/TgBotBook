import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.menu_kb import set_main_menu
import os


# инициализация логгера
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    encoding='utf-8',
    filename=os.path.normpath("logs/log.logs"),
    filemode="a",
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
       '%(lineno)d - %(name)s - %(message)s'
)


async def main():
    # сообщение в логи о запуске бота
    logger.warning("Бот запущен.")

    # инициализация конфига
    config: Config = load_config()  
    logger.info("Конфиг инициализирован.")

    # инициализация бота и диспетчера
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    logger.info("Бот и диспетчер инициализированы.")

    # регистрация роутеров
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    logging.info("Роутеры инициализированы.")

    # подключение главного меню бота
    await set_main_menu(bot)

    # пропуск накопившихся апдейтов и запуск полинга
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
