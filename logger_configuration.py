import logging
from sources.exceptions import IncorrectLoggerConfiguration


format = "%(asctime)s %(name)s %(levelname)s:%(message)s"


def configure_logger(level: str) -> None:
    if level == "ERROR":
        logging.basicConfig(level=logging.ERROR, format=format)

    elif level == "INFO":
        logging.basicConfig(level=logging.INFO, format=format)

    elif level == "DEBUG":
        logging.basicConfig(level=logging.DEBUG, format=format)

    else:
        raise IncorrectLoggerConfiguration("Такой уровень, logger не поддерживает!")
