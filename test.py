from fastapi.testclient import TestClient

from fastapi import FastAPI
from core import XenXenXenSeCore

from sys import argv

app = FastAPI(
    title="Xen API v2",
    description="XenServer Management API to REST API",
    debug=True
)

XXXS_core = XenXenXenSeCore(app)
XXXS_app = XXXS_core.app

client = TestClient(XXXS_app)


cluster_id = "crongcloud"

def test_host_list():
    response = client.get("/v1/"+cluster_id+"/host/list")
    assert response.status_code == 200
    print("OK")

def test_vm_list():
    response = client.get("/v1/"+cluster_id+"/vm/list")
    assert response.status_code == 200
    print("OK")

if __name__ == "__main__":
    print("XenXenXenSei: Unit Test for GitHub Actions")
    print()

    try:
        print("Testing /host/list ...", end='')
        test_host_list()

        print("Testing /vm/list ...", end='')
        test_vm_list()

        print("Test success!")
    except Exception:
        print("test failed!!!!")
        exit(1)
