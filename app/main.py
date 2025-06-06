import logging

from bot.bot import bot
from db.db import CreateDB
from utils import get_logger
from utils.constant import NEED_CREATE_DB

logger = get_logger()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
        level=logging.INFO,
    )
    if isinstance(NEED_CREATE_DB, str) and NEED_CREATE_DB == "True":
        logger.info("Инициализация DB")
        CreateDB()
    logger.info("Starting bot ...")
    bot.infinity_polling()
