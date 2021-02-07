import sys

import uvicorn
from fastapi.testclient import TestClient

from API import router as _api_router
from app.services import Server
from app.services.info import Info

log_config = uvicorn.config.LOGGING_CONFIG

app = Server(
    ctx="",
    host="127.0.0.1",
    port=8080,
    title=Info.get_name(),
    description=Info.get_description(),
    fast_api_debug=True,
    asgi_debug=False,
    log_config=log_config,
)

app.include_router(_api_router)

client = TestClient(app)


cluster_id = "crongcloud"


def test_host_list():
    response = client.get("/v1/" + cluster_id + "/host/list")
    assert response.status_code == 200
    print("OK")


def test_vm_list():
    response = client.get("/v1/" + cluster_id + "/vm/list")
    assert response.status_code == 200
    print("OK")


def test_vdi_list():
    response = client.get("/v1/" + cluster_id + "/vdi/list")
    assert response.status_code == 200
    print("OK")


if __name__ == "__main__":

    from pyfiglet import Figlet

    figlet = Figlet()

    print(figlet.renderText("XenXenXenSe"))

    print(
        "Project XenXenXenSe : a RESTful API implementation for Citrix Hypervisor® and XCP-ng"
    )
    print("Unit Test Script")
    print()
    print("Copyright (c) Stella IT.")
    print("This software is distributed under MIT License.")
    print()
    print("Warning: This software is supposed to be used with GitHub Actions.")
    print(
        "         This software is supposed to test against Stella IT's Internal Cloud Infrastructure Test Servers."
    )
    print()
    print()

    try:
        print("Testing /host/list against test cluster ...", end="")
        test_host_list()

        print("Testing /vm/list against test cluster ...", end="")
        test_vm_list()

        print("Testing /vdi/list against test cluster ...", end="")
        test_vdi_list()

        print("Test success!")
    except Exception:
        print("test failed!!!!")
        sys.exit(1)
