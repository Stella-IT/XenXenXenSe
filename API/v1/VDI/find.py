from fastapi import APIRouter

from API.v1.Interface import NameArgs

from XenGarden.VDI import VDI
from XenGarden.session import create_session

from .serialize import serialize

router = APIRouter()


@router.post("/{cluster_id}/vdi/find")
async def find_VDI_by_name(cluster_id: str, args: NameArgs):
    """ Find VDI by Name """
    session = create_session(cluster_id)
    name = args.name
    vdis = VDI.get_by_name(session, name)

    if vdis is not None:
        vdis_list = []
        for vdi in vdis:
            vdis_list.append(serialize(vdi))

        ret = {"success": True, "data": vdis_list}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vdi/find/{iso_name}")
async def insert_cd_inurl_name(cluster_id: str, iso_name: str):
    """ Find VDI by Name """
    session = create_session(cluster_id)
    vdis = VDI.get_by_name(session, iso_name)
    print(vdis)

    if vdis is not None:
        vdis_list = []
        for vdi in vdis:
            vdis_list.append(serialize(vdi))

        ret = {"success": True, "data": vdis_list}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret
