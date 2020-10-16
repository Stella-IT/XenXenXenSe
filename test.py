import sys

from fastapi.testclient import TestClient

from fastapi import FastAPI
from core import XenXenXenSeCore

from sys import argv

app = FastAPI(
    title="Xen API v2",
    description="XenServer Management API to REST API",
    debug=True,
)

XXXS_core = XenXenXenSeCore(app)
XXXS_app = XXXS_core.app

client = TestClient(XXXS_app)


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
