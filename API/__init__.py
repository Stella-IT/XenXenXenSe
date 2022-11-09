from fastapi import APIRouter, Depends

from API.v1 import v1_router as _v1_router
from app.services.info import Info
from app.security import Security
from app.settings import Settings

from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(dependencies=[Depends(Security.run_authentication)])

_v1_prefix = "/v1"
router.include_router(_v1_router, prefix=_v1_prefix)

@router.get("/")
async def root():
    xen_clusters = Settings.get_xen_clusters()
    xen_cluster_names = [xen_cluster for xen_cluster in xen_clusters]

    title = Info.get_name()
    description = Info.get_description()
    version = Info.get_version()

    return {
        "hello": "world",
        "about": {"name": title, "description": description, "version": version},
        "clusters": xen_cluster_names,
    }
