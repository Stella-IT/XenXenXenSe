from fastapi import APIRouter

from app.settings import Settings

from .model._root import XXXS_V1_Root

root_router = APIRouter()


@root_router.get("/", response_model=XXXS_V1_Root)
async def v1_root():
    xen_clusters = Settings.get_xen_clusters()
    xen_cluster_names = [xen_cluster for xen_cluster in xen_clusters]

    return {
        "hello": "world",
        "api": {"version": 1, "name": "XenXenXenSe"},
        "clusters": xen_cluster_names,
    }
