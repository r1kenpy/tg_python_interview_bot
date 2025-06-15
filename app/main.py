import logging

from bot.bot import bot

# from db.db import WorkingWithDB
from utils import get_logger

logger = get_logger()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
        level=logging.INFO,
    )
    logger.info("Starting bot ...")
    bot.infinity_polling()
