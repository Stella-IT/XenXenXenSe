import logging
import sys
from pathlib import Path

import ujson
from loguru import logger

from app.extension.logging.interceptHandler import InterceptHandler


class CustomizeLogger:
    @classmethod
    def make_logger(cls):
        config_path = "logging_config.json"
        config = cls.load_logging_config(config_path)
        logging_config = config["logger"]

        _logger = cls.customize_logging(
            filepath=logging_config["path"] + logging_config["filename"],
            level=logging_config["level"],
            retention=logging_config["retention"],
            rotation=logging_config["rotation"],
            format=logging_config["format"],
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
            sink=str(filepath),
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
    def load_logging_config(cls, config_path: str) -> dict:
        """

        :param config_path:
        :type config_path:
        :return: logging config
        :rtype: dict
        """
        conf_path = config_path
        with open(conf_path, "r") as config_file:
            conf = ujson.load(config_file)
        return conf
