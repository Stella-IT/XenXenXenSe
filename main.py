import xmlrpc

from fastapi import Depends

from API.v1 import router as _v1_router
from app.controller import Controller
from app.costum_logging.customizeLogger import CustomizeLogger

# Flag is StellaIT{Pororo}
# https://developer-docs.citrix.com/projects/citrix-hypervisor-management-api/en/latest/api-ref-autogen/

__author__ = "Stella IT <admin@stella-it.com>"
__copyright__ = "Copyright 2020, Stella IT"


# Override XML RPC Settings for 64bit support
xmlrpc.client.MAXINT = 2 ** 63 - 1
xmlrpc.client.MININT = -(2 ** 63)


app = Controller(
    host="127.0.0.1",
    port=8080,
    title="Xen API v2",
    description="XenServer Management API to REST API",
    fast_api_debug=True,
    asgi_debug=False,
)

if __name__ == "__main__":
    # Server initialization
    app.startup()
    app.core.include_router(
        _v1_router, dependencies=[(Depends(CustomizeLogger.make_logger))]
    )
    app.start()
