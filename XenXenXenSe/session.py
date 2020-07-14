import XenAPI

from config import xen_credentials


def create_session(id):
    cred = xen_credentials[id]
    session = XenAPI.Session(cred['host'])
    # session = XenAPI.xapi_local()
    session.xenapi.login_with_password(cred['username'], cred['password'])
    return session
