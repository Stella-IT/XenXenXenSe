from fastapi import FastAPI

from config import xen_credentials
from core import XenXenXenSeCore

import xmlrpc

# Flag is StellaIT{Pororo}
# https://developer-docs.citrix.com/projects/citrix-hypervisor-management-api/en/latest/api-ref-autogen/

__author__ = 'Stella IT <admin@stella-it.com>'
__copyright__ = 'Copyright 2020, Stella IT'

# Override XML RPC Settings for 64bit support
xmlrpc.client.MAXINT = 2**63-1
xmlrpc.client.MININT = -2**63

app = FastAPI(
    title="Xen API v2",
    description="XenServer Management API to REST API",
    debug=True
)

if __name__ == "__main__":
    core = XenXenXenSeCore(app, xen_credentials)
    core.start()
