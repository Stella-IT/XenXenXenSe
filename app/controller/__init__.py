import asyncio
from asyncio import AbstractEventLoop
from typing import Optional

from app.services.console import Console
from app.services.info import Info
from app.services.server import Server


class Controller:
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8080,
        sock: Optional[str] = None,
        title: str = "",
        description: str = "",
        dependencies: Optional[list] = None,
        log_config=None,
        fast_api_debug: bool = False,
        asgi_debug: bool = False,
        version: str = Info.get_version(),
        loop: Optional[AbstractEventLoop] = None,
        quiet: bool = False,
    ) -> None:
        self.loop = loop or self._loop()
        self.host = host
        self.port = port
        self.sock = sock
        self.title = title
        self.description = description
        self.dependencies = dependencies
        self.log_config = log_config
        self.fast_api_debug = fast_api_debug
        self.asgi_debug = asgi_debug
        self.version = version
        self.quiet = quiet
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
            sock=self.sock,
            title=self.title,
            description=self.description,
            dependencies=self.dependencies,
            log_config=self.log_config,
            asgi_debug=self.asgi_debug,
            debug=self.fast_api_debug,
            version=self.version,
        )

    def start(self) -> None:
        try:
            if not self.quiet:
                self.__console().show_banner(True)
                self.__console().print_xen_hostnames(True)

            asyncio.ensure_future(self.core.make_process(), loop=self.loop)
            self.loop.run_forever()
        except TypeError as e:
            raise e
            pass
