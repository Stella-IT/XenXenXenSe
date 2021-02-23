import asyncio

from XenGarden.SR import SR

async def serialize(sr: SR):
    return dict(
        name=sr.get_name(),
        description=sr.get_description(),
        size=sr.get_physical_size(),
        used=sr.get_physical_utilisation(),
        free=str(int(sr.get_physical_size()) - int(sr.get_physical_utilisation())),
        uuid=sr.get_uuid(),
        content_type=sr.get_content_type(),
        type=sr.get_type(),
    )
