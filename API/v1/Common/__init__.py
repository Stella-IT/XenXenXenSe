from XenAPI.XenAPI import Failure


def xenapi_failure_jsonify(failure: Failure):
    return {
        "type": "xenapi",
        "error": {"name": failure.details[0], "details": failure.details[1:]},
    }
