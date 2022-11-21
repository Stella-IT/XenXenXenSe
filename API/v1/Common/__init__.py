from XenAPI.XenAPI import Failure

from app.controller import Controller


def xenapi_failure_jsonify(failure: Failure):
    return {
        "type": "xenapi",
        "error": {"name": failure.details[0], "details": failure.details[1:]},
        "exception": Controller._serialize_exception(failure),
    }
