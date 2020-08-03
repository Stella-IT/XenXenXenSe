from XenXenXenSe.Console import Console


def serialize(console: Console):
    return {
        "location": console.get_location(),
        "protocol": console.get_protocol(),
        "uuid": console.get_uuid(),
    }
