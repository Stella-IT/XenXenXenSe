from fastapi import APIRouter

from XenGarden.SR import SR
from XenGarden.session import create_session

from API.v1.SR.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/sr/list")
async def sr_list(cluster_id: str):
    """ Get All from Storage Repos """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    srs = SR.get_all(session=session)

    __sant_sr = []
    sant_sr = __sant_sr.append
    for sr in srs:
        sant_sr(serialize(sr))

    ret = dict(success=True, data=__sant_sr)

    session.xenapi.session.logout()
    return ret
