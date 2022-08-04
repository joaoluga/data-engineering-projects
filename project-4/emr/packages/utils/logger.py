from __future__ import annotations

import logging
import sys


class Logger:
    def __init__(self):
        self.__logger = logging.getLogger()
        self.__configuration_settings()

    def __configuration_settings(self):
        msg_format = "[%(asctime)s][%(module)s - %(funcName)s at line %(lineno)d][%(levelname)s]: %(message)s"

        self.__logger.setLevel(logging.INFO)
        logger_formatter = logging.Formatter(msg_format, datefmt="%Y-%m-%d %H:%M:%S")
        default_handler = logging.StreamHandler(sys.stdout)
        default_handler.setFormatter(logger_formatter)

        if not self.__logger.handlers:
            self.__logger.addHandler(default_handler)
        else:
            self.__logger.removeHandler(self.__logger.handlers[0])
            self.__logger.addHandler(default_handler)

    def info(self, message: str):
        self.__logger.info(message)

    def warning(self, message: str):
        self.__logger.warning(message)

    def error(self, message: str):
        self.__logger.error(message)
