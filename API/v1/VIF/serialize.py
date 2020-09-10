from XenGarden.VIF import VIF

from API.v1.VM.serialize import serialize as _vm_serialize


def serialize(vif: VIF):
    vm = vif.get_vm()
    if vm is not None:
        vm = _vm_serialize(vm)

    return dict(
        attached=vif.get_attached(),
        vm=vm,
        uuid=vif.get_uuid(),
        mac=vif.get_mac(),
        mtu=vif.get_mtu(),
        qos=dict(
            type=vif.get_qos_type(),
            info=vif.get_qos_info(),
            supported=vif.supported_qos_types()
        ),
        ipv4=dict(
            address=vif.get_address_v4(),
            gateway=vif.get_gateway_v4()
        ),
        ipv6=dict(
            address=vif.get_address_v6(),
            gateway=vif.get_gateway_v6()
        )
    )
