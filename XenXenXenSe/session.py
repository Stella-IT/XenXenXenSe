import XenAPI

from config import xen_credentials


def create_session(_id):
    cred = xen_credentials[_id]
    session = XenAPI.Session(cred['_host'])
    # session = XenAPI.xapi_local()
    session.xenapi.login_with_password(cred['username'], cred['password'])
    return session
