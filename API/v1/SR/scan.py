from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.SR import SR

from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/sr/{sr_uuid}/scan")
async def sr_scan(cluster_id: str, sr_uuid: str):
    """ Scan Storage Repository """
    try:
        session = create_session(
            cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        sr: SR = SR.get_by_uuid(session=session, uuid=sr_uuid)

        if sr is not None:
            sr.scan()
            ret = dict(success=True)
        else:
            ret = dict(success=False)

        session.xenapi.session.logout()
        return ret
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)
