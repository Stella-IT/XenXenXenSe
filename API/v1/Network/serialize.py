from XenGarden.Network import Network


async def serialize(network: Network):
    return dict(
        uuid=network.get_uuid(),
        name=network.get_name(),
        description=network.get_description(),
        mtu=network.get_mtu(),
    )
