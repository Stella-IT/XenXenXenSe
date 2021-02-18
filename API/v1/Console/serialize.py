from XenGarden.Console import Console


async def serialize(console: Console):
    record = console.get_record()

    return dict(
        location=record["location"],
        protocol=record["protocol"],
        uuid=record["uuid"],
    )
