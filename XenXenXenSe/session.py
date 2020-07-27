import XenAPI

from config import get_xen_clusters


def create_session(_id):
    xen_clusters = get_xen_clusters()

    cred = xen_clusters[_id]
    session = XenAPI.Session(cred['host'])
    # session = XenAPI.xapi_local()
    session.xenapi.login_with_password(cred['username'], cred['password'])
    return session
