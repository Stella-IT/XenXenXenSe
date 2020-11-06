import asyncio

from MySQLdb._exceptions import OperationalError

from app.console import Console
from app.service import Initializer, Schedule, Server
from MySQL import DatabaseCore, init_connection


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

    def initialize(self):
        self.sc = Schedule()

    def sync_mysql_database(self):
        self.smd = Initializer()
        return self.smd

    def mysql_process(self):
        self.manager = DatabaseCore()
        return self.manager

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

        @self.core.on_event("startup")
        async def on_startup() -> None:
            """database connection"""
            try:
                self.manager.metadata.create_all(self.manager.create_engine)
                if not self.manager.database.is_connected:
                    await self.manager.database.connect()
            except AttributeError or OperationalError:
                pass

        @self.core.on_event("shutdown")
        async def on_shutdown() -> None:
            """database disconnection"""
            if self.manager.metadata.is_connected:
                await self.manager.database.disconnect()

    def start(self):
        try:
            self.init_console().show_banner(True)
            self.init_console().print_xen_hostnames(True)
            self.sync_mysql_database().db_migration()
            init_connection()
            asyncio.ensure_future(self.core.make_process(), loop=self.loop())
            asyncio.ensure_future(self.sc.initialize(), loop=self.loop())
            self.loop.run_forever()
        except TypeError:
            pass
