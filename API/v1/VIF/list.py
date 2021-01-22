from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter
from fastapi import HTTPException
from XenGarden.session import create_session
from XenGarden.VIF import VIF

from API.v1.VIF.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vif/list")
async def vif_list(cluster_id: str):
    """ Get All from Storage Repos """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vifs = VIF.get_all(session=session)

        __santilized_vifs = []
        santilized_vifs = __santilized_vifs.append
        for vif in vifs:
            santilized_vifs(serialize(vif))

        ret = dict(success=True, data=__santilized_vifs)

        session.xenapi.session.logout()
        return ret
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)
