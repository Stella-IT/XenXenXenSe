from fastapi import APIRouter

from API.v1.Interface import NameArgs

from XenXenXenSe.SR import SR
from XenXenXenSe.session import create_session

from .serialize import serialize

router = APIRouter()


@router.post("/{cluster_id}/sr/find")
async def find_cd_by_name(cluster_id: str, args: NameArgs):
    """ Find SR by Name """
    session = create_session(cluster_id)
    name = args.name
    srs = SR.get_by_name(session, name)

    srs_list = []
    for sr in srs:
        srs_list.append(serialize(sr))

    if sr is not None:
        ret = {"success": True, "data": srs_list}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/sr/find/{iso_name}")
async def insert_cd_inurl_name(cluster_id: str, iso_name: str):
    """ Find SR by Name """
    session = create_session(cluster_id)
    srs = SR.get_by_name(session, iso_name)

    if srs is not None:
        srs_list = []
        for sr in srs:
            srs_list.append(serialize(sr))

        ret = {"success": True, "data": srs_list}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret
