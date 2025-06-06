import logging


def _basic_config() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",
    )


def get_logger(name="interbot", level=logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level=level)
    return logger
