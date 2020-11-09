from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.Interface import DescriptionArgs, NameArgs
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/name")
@router.get("/{cluster_id}/template/{vm_uuid}/name")
async def instance_get_name(cluster_id: str, vm_uuid: str):
    """ Get Instance (VM/Template) Name """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        if _vm is not None:
            ret = dict(success=True, data=_vm.get_name())
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


@router.get("/{cluster_id}/vm/{vm_uuid}/description")
@router.get("/{cluster_id}/template/{vm_uuid}/description")
async def instance_get_description(cluster_id: str, vm_uuid: str):
    """ Get Instance (VM/Template) Description (needs troubleshooting) """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        if _vm is not None:
            ret = dict(success=True, data=_vm.get_description())
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


@router.put("/{cluster_id}/vm/{vm_uuid}/name")
@router.put("/{cluster_id}/template/{vm_uuid}/name")
async def instance_set_name(cluster_id: str, vm_uuid: str, args: NameArgs):
    """ Set Instance (VM/Template) Name """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        if _vm is not None:
            ret = dict(success=_vm.set_name(args.name))
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


@router.get("/{cluster_id}/vm/{vm_uuid}/name/{new_name}")
@router.get("/{cluster_id}/template/{vm_uuid}/name/{new_name}")
async def instance_set_name_inurl(
    cluster_id: str, vm_uuid: str, new_name: str
):
    """ Set Instance (VM/Template) Name """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        if _vm is not None:
            ret = dict(success=_vm.set_name(new_name))
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


@router.put("/{cluster_id}/vm/{vm_uuid}/description")
@router.put("/{cluster_id}/template/{vm_uuid}/description")
async def instance_set_description(
    cluster_id: str, vm_uuid: str, args: DescriptionArgs
):
    """ Set Instance (VM/Template) Description """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        if _vm is not None:
            ret = dict(success=_vm.set_description(args.description))
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


@router.get("/{cluster_id}/vm/{vm_uuid}/description/{new_description}")
@router.get("/{cluster_id}/template/{vm_uuid}/description/{new_description}")
async def instance_set_description_inurl(
    cluster_id: str, vm_uuid: str, new_description: str
):
    """ Set Instance (VM/Template) Description """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        if _vm is not None:
            ret = dict(success=_vm.set_description(new_description))
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
