import xmlrpc

import uvicorn
from fastapi.responses import UJSONResponse

from API import router as _api_router
from app.controller import Controller
from app.extension import CustomizeLogger
from app.services.console import Console
from app.services.info import Info

# Flag is StellaIT{Pororo}
# https://developer-docs.citrix.com/projects/citrix-hypervisor-management-api/en/latest/api-ref-autogen/

__author__ = "Stella IT <admin@stella-it.com>"
__copyright__ = "Copyright 2020-2021 Stella IT"
__version__ = Info.get_version()

# Override XML RPC Settings for 64bit support
xmlrpc.client.MAXINT = 2**63 - 1
xmlrpc.client.MININT = -(2**63)

uvicorn_log_config = uvicorn.config.LOGGING_CONFIG
del uvicorn_log_config["loggers"]["uvicorn"]

# command line parser
parser = Console.create_parser()

# Main Process
if __name__ == "__main__":
    args = parser.parse_args()
    debug_mode = args.debug_mode

    if args.show_version:
        print(__version__)
        exit()

    # Create an application
    app = Controller(
        host=args.host,
        port=args.port,
        sock=args.sock,
        title=Info.get_name(),
        description=Info.get_description(),
        fast_api_debug=args.debug_mode,
        asgi_debug=args.debug_mode,
        log_config=uvicorn_log_config,
        quiet=args.quiet_mode,
    )

    # Server initialization
    app.startup()
    app.core.add_event_handler("startup", CustomizeLogger.make_logger)
    app.core.include_router(
        _api_router,
        default_response_class=UJSONResponse,
    )
    app.start()
