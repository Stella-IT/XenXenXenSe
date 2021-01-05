import uvicorn
from fastapi import FastAPI, Depends
from app.extension import CustomizeLogger


class Server(FastAPI):
    def __init__(
        self,
        ctx,
        host: str,
        port: int,
        title: str,
        description: str,
        log_config,
        asgi_debug: bool = False,
        debug: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self.controller = ctx

        # ASGI Server configuration parameters
        self.server = uvicorn
        self._host = host
        self._port = port
        self._title = title
        self._description = description
        self.dependencies = [Depends(CustomizeLogger.make_logger())]
        self._log_config = log_config
        self._debug = debug
        self._asgi_debug = asgi_debug
        super().__init__(*args, **kwargs)

    def make_process(self) -> None:
        return self.server.run(
            app=self, host=self._host, port=self._port, debug=self._asgi_debug, log_config=self._log_config
        )
