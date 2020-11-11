import asyncio

from app.console import Console
from app.service import Server


class Controller:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
        title: str = "",
        description: str = "",
        fast_api_debug: bool = False,
        asgi_debug: bool = False,
        loop=None,
    ):
        self.loop = loop or self._loop()
        self.host = host
        self.port = port
        self.title = title
        self.description = description
        self.fast_api_debug = fast_api_debug
        self.asgi_debug = asgi_debug
        self.manager = None
        self.core = None
        self.smd = None
        self.sc = None

    @staticmethod
    def _loop():
        return asyncio.get_event_loop()

    # @property
    # def logger(self):
    #    return logging.getLogger(
    #        f"{self.__class__.__module__}: {self.__class__.__name__}"
    #    )

    @staticmethod
    def init_console():
        co = Console()
        return co

    def startup(self):
        self.core = Server(
            ctx=self,
            host=self.host,
            port=self.port,
            title=self.title,
            description=self.description,
            asgi_debug=self.asgi_debug,
            debug=self.fast_api_debug,
        )

    def start(self):
        try:
            self.init_console().show_banner(True)
            self.init_console().print_xen_hostnames(True)
            asyncio.ensure_future(self.core.make_process(), loop=self.loop())
            self.loop.run_forever()
        except TypeError:
            pass
