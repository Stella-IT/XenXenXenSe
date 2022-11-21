import asyncio
import logging
from asyncio import AbstractEventLoop
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

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
        **kwargs,
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
        self._sentry_dsn = kwargs.get("sentry_dsn")

    @staticmethod
    def _loop() -> AbstractEventLoop:
        return asyncio.get_event_loop()

    @staticmethod
    def __console() -> Console:
        return Console()

    def _initialize_sentry(self):
        if self._sentry_dsn is not None:
            try:
                import sentry_sdk

                sentry_sdk.init(
                    dsn=self._sentry_dsn,
                    traces_sample_rate=1.0,
                )

                return True
            except ImportError:
                return False

        return None

    def startup(self) -> None:
        self._initialize_sentry()

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

        @self.core.exception_handler(Exception)
        async def _fake_exception_handler(req: Request, exception: Exception):
            return self.exception_handler(req, exception)

    def exception_handler(self, req: Request, exception: Exception):
        exception_data = self.core._exception_to_json(exception)
        debug_data = {}

        if exception_data is not None:
            debug_data["exception"] = exception_data

        if type(exception) == HTTPException:
            return JSONResponse(
                status_code=exception.status_code,
                content={**exception.details, **debug_data},
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"type": "exception", **debug_data},
            )

    def start(self) -> None:
        try:
            if not self.quiet:
                self.__console().show_banner(True)
                self.__console().print_xen_hostnames(True)

            asyncio.ensure_future(self.core.make_process(), loop=self.loop)
            self.loop.run_forever()
        except TypeError as e:
            pass
