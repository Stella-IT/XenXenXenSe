from fastapi import APIRouter

from XenXenXenSe.VBD import VBD
from XenXenXenSe.VDI import VDI
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/vbd/{vbd_uuid}/insert/{vdi_uuid}")
async def vbd_insert_vdi_by_uuid(cluster_id: str, vbd_uuid: str, vdi_uuid: str):
    """ Insert VDI into VBD by UUID """
    session = create_session(cluster_id)
    vdi: VDI = VDI.get_by_uuid(session, vdi_uuid)

    if vdi is None:
        ret = {"success": False}
        session.xenapi.session.logout()
        return ret

    vbd: VBD = VBD.get_by_uuid(session, vbd_uuid)

    if vbd is not None:
        ret = {"success": vbd.insert(vdi)}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.delete("/{cluster_id}/vbd/{vbd_uuid}/insert")
@router.get("/{cluster_id}/vbd/{vbd_uuid}/eject")
async def vbd_eject_vdi(cluster_id: str, vbd_uuid: str):
    """ Eject VDI from VBD """
    session = create_session(cluster_id)
    vbd: VBD = VBD.get_by_uuid(session, vbd_uuid)

    if vbd is not None:
        ret = {"success": vbd.eject()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret
