from XenGarden.Console import Console


async def serialize(console: Console):
    return dict(
        location=console.get_location(),
        protocol=console.get_protocol(),
        uuid=console.get_uuid(),
    )
