import logging
import sys
from pathlib import Path

import ujson
from loguru import logger

from app.costum_logging.interceptHandler import InterceptHandler


class CustomizeLogger:
    @classmethod
    def make_logger(cls):
        """

        :param config_path:
        :type config_path:
        :return:
        :rtype:
        """
        config_path = "logging_config.json"
        config = cls.load_logging_config(config_path)
        logging_config = config.get("logger")

        _logger = cls.customize_logging(
            filepath=logging_config.get("path"),
            level=logging_config.get("level"),
            retention=logging_config.get("retention"),
            rotation=logging_config.get("rotation"),
            format=logging_config.get("format"),
        )
        return _logger

    @classmethod
    def customize_logging(
        cls,
        filepath: Path,
        level: str,
        rotation: str,
        retention: str,
        format: str,
    ):
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
        )
        logger.add(
            str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
        )
        # noinspection PyArgumentList
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)

    @classmethod
    def load_logging_config(cls, config_path) -> dict:
        """

        :param config_path:
        :type config_path:
        :return: logging config
        :rtype: dict
        """

        config = None
        with open(config_path) as config_file:
            config = ujson.load(config_file)
        return config
