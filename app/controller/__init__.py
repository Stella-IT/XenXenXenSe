import asyncio
from asyncio import AbstractEventLoop
from typing import List, Optional

from fastapi import Depends

from app.services.console import Console
from app.services.server import Server


class Controller:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
        title: str = "",
        description: str = "",
        dependencies: Optional[list] = None,
        log_config=None,
        fast_api_debug: bool = False,
        asgi_debug: bool = False,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        self.loop = loop or self._loop()
        self.host = host
        self.port = port
        self.title = title
        self.description = description
        self.dependencies = dependencies
        self.log_config = log_config
        self.fast_api_debug = fast_api_debug
        self.asgi_debug = asgi_debug
        self.core: Optional[Server] = None

    @staticmethod
    def _loop() -> AbstractEventLoop:
        return asyncio.get_event_loop()

    @staticmethod
    def __console() -> Console:
        return Console()

    def startup(self) -> None:
        self.core = Server(
            ctx=self,
            host=self.host,
            port=self.port,
            title=self.title,
            description=self.description,
            dependencies=self.dependencies,
            log_config=self.log_config,
            asgi_debug=self.asgi_debug,
            debug=self.fast_api_debug,
        )

    def start(self) -> None:
        try:
            self.__console().show_banner(True)
            self.__console().print_xen_hostnames(True)
            asyncio.ensure_future(self.core.make_process(), loop=self.loop)
            self.loop.run_forever()
        except TypeError:
            pass

    def register_dependency(self, dependency) -> None:
        if self.dependencies is None:
            self.dependencies = []

        self.dependencies.append(dependency)
