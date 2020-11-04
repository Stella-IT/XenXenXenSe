from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.SR import SR

from API.v1.Interface import NameArgs
from API.v1.SR.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.post("/{cluster_id}/sr/find")
async def find_cd_by_name(cluster_id: str, args: NameArgs):
    """ Find SR by Name """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        name = args.name
        srs = SR.get_by_name(session=session, name=name)

        sr = None

        __srs_list = []
        srs_list = __srs_list.append
        for sr in srs:
            srs_list(serialize(sr))

        if sr is not None:
            ret = dict(success=True, data=__srs_list)
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


@router.get("/{cluster_id}/sr/find/{iso_name}")
async def insert_cd_inurl_name(cluster_id: str, iso_name: str):
    """ Find SR by Name """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        srs = SR.get_by_name(session=session, name=iso_name)

        if srs is not None:
            __srs_list = []
            srs_list = __srs_list.append
            for sr in srs:
                srs_list(serialize(sr))

            ret = dict(success=True, data=__srs_list)
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
