import sys

from fastapi.testclient import TestClient

from API.v1 import router as _v1_router
from app.service import Server

app = Server(
    ctx="",
    host="127.0.0.1",
    port=8080,
    title="Xen API v2",
    description="XenServer Management API to REST API",
    fast_api_debug=True,
    asgi_debug=False,
)

app.include_router(_v1_router)

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
    print("This software is distributed under Affero GNU Public License v3.")
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

        print("Test success!")
    except Exception:
        print("test failed!!!!")
        sys.exit(0)
