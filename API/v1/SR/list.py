from fastapi import APIRouter

from XenGarden.SR import SR
from XenGarden.session import create_session

from .serialize import serialize

router = APIRouter()


@router.get("/{cluster_id}/sr/list")
async def sr_list(cluster_id: str):
    """ Get All from Storage Repos """
    session = create_session(cluster_id)
    srs = SR.get_all(session)

    sant_sr = []
    for sr in srs:
        sant_sr.append(serialize(sr))

    ret = {"success": True, "data": sant_sr}

    session.xenapi.session.logout()
    return ret
