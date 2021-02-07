from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.VIF.serialize import serialize as _vif_serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/vif")
async def instance_vif(cluster_id: str, vm_uuid: str):
    """ Show Instnace VIFs """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

        if vm is not None:

            new_vif = vm.get_VIF()

            if new_vif is not None:

                ret = dict(success=True, data=_vif_serialize(new_vif))
            else:
                ret = dict(success=False)
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


@router.get("/{cluster_id}/vm/{vm_uuid}/vif/qos")
async def vif_get_qos_by_uuid(cluster_id: str, vm_uuid: str):
    """ Set VIF QoS by VM """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

        if vm is not None:

            vif = vm.get_VIF()

            if vif is not None:
                ret = dict(
                    success=True,
                    data=dict(type=vif.get_qos_type(), info=vif.get_qos_info()),
                )
            else:
                ret = dict(success=False)

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


@router.get("/{cluster_id}/vm/{vm_uuid}/vif/qos/speed/{speed}")
async def vif_set_qos_speed_by_vm(cluster_id: str, vm_uuid: str, speed: str):
    """ Set VIF QoS Speed by VM """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

        if vm is not None:

            vif = vm.get_VIF()

            try:
                speedNum = int(speed)
            except ValueError:
                return dict(success=False)

            if speedNum <= 0:
                a = vif.set_qos_type("")
                b = vif.set_qos_info({})

                ret = dict(success=a and b)

            else:
                if vif is not None:
                    if vif.get_qos_type() != "ratelimit":
                        vif.set_qos_type("ratelimit")

                    ret = dict(success=vif.set_qos_info(dict(kbps=speed)))
                else:
                    ret = dict(success=False)

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


@router.get("/{cluster_id}/vm/{vm_uuid}/vifs")
async def instance_vifs(cluster_id: str, vm_uuid: str):
    """ Show Instnace VIFs """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

        if vm is not None:

            new_vifs = vm.get_VIFs()

            __vif_serialized = []

            if new_vifs is not None:
                for vif in new_vifs:
                    if vif is not None:
                        __vif_serialized.append(_vif_serialize(vif))

                ret = dict(success=True, data=__vif_serialized)
            else:
                ret = dict(success=False)
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
