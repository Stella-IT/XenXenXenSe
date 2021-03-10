import logging
import os
import sys
from pathlib import Path

import ujson
from loguru import logger

from app.extension.logging.interceptHandler import InterceptHandler

default_config = {
    "path": "./logs",
    "filename": "x3s_access.log",
    "level": "info",
    "rotation": "20 days",
    "retention": "1 months",
    "format": "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> request id: {extra[request_id]} - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
}


class CustomizeLogger:
    default_config_path = "logging_config.json"

    @classmethod
    def make_logger(cls, config_path=default_config_path):
        logging_config = default_config

        if os.path.exists(config_path):
            config = cls.load_logging_config(config_path)
            logging_config = config["logger"]

        filepath = Path(logging_config["path"])
        filepath.mkdir(0o777, True, True)

        filepath = filepath.joinpath(logging_config["filename"])

        _logger = cls.customize_logging(
            filepath=filepath,
            level=logging_config["level"],
            retention=logging_config["retention"],
            rotation=logging_config["rotation"],
            _format=logging_config["format"],
        )

        return _logger

    @classmethod
    def customize_logging(
        cls,
        filepath: Path,
        level: str,
        rotation: str,
        retention: str,
        _format: str,
    ):
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=_format,
        )
        logger.add(
            sink=str(filepath),
            rotation=rotation,
            retention=retention,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=_format,
        )

        # noinspection PyArgumentList
        # logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ["fastapi", "uvicorn", "uvicorn.error"]:
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
