from XenGarden.PIF import PIF


async def serialize(pif: PIF):
    return dict(
        attached=pif.get_attached(),
        uuid=pif.get_uuid(),
        mac=pif.get_mac(),
        mtu=pif.get_mtu(),
        device=pif.get_device(),
        ipv4=dict(address=pif.get_address_v4(), gateway=pif.get_gateway_v4()),
        ipv6=dict(address=pif.get_address_v6()),
    )
