from XenGarden.VIF import VIF


async def serialize(vif: VIF):
    from API.v1.VM.serialize import serialize as _vm_serialize
    from API.v1.Network.serialize import serialize as _network_serialize

    vm = vif.get_vm()
    if vm is not None:
        vm = await _vm_serialize(vm)

    network = vif.get_network()
    if network is not None:
        network = await _network_serialize(network)

    return dict(
        attached=vif.get_attached(),
        vm=vm,
        network=network,
        uuid=vif.get_uuid(),
        mac=vif.get_mac(),
        mtu=vif.get_mtu(),
        qos=dict(
            type=vif.get_qos_type(),
            info=vif.get_qos_info(),
            supported=vif.supported_qos_types(),
        ),
        device=vif.get_device(),
        locking_mode=vif.get_locking_mode(),
        ipv4=dict(address=vif.get_address_v4(), gateway=vif.get_gateway_v4()),
        ipv6=dict(address=vif.get_address_v6(), gateway=vif.get_gateway_v6()),
    )
