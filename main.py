import xmlrpc

import uvicorn
from fastapi import Depends
from fastapi.responses import UJSONResponse

from API.v1 import router as _v1_router
from app.controller import Controller
from app.extension import CustomizeLogger

# Flag is StellaIT{Pororo}
# https://developer-docs.citrix.com/projects/citrix-hypervisor-management-api/en/latest/api-ref-autogen/

__author__ = "Stella IT <admin@stella-it.com>"
__copyright__ = "Copyright 2020, Stella IT"


# Override XML RPC Settings for 64bit support
xmlrpc.client.MAXINT = 2 ** 63 - 1
xmlrpc.client.MININT = -(2 ** 63)

uvicorn_log_config = uvicorn.config.LOGGING_CONFIG
del uvicorn_log_config["loggers"]["uvicorn"]

app = Controller(
    host="127.0.0.1",
    port=8080,
    title="Xen API v2",
    description="XenServer Management API to REST API",
    fast_api_debug=True,
    asgi_debug=False,
    log_config=uvicorn_log_config,
)


if __name__ == "__main__":
    # Server initialization
    app.startup()
    app.dependencies = [Depends(CustomizeLogger.make_logger())]
    app.core.include_router(
        _v1_router,
        default_response_class=UJSONResponse,
        dependencies=[Depends(CustomizeLogger.make_logger)],
    )
    app.start()
