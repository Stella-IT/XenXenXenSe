import sys

import uvicorn
from fastapi import FastAPI
from threading import Thread

import schedule
import time
import signal

from API.v1 import router as _v1_router

from config import xen_credentials
from MySQL import init_connection

import xmlrpc

# Flag is StellaIT{Pororo}
# https://developer-docs.citrix.com/projects/citrix-hypervisor-management-api/en/latest/api-ref-autogen/

__author__ = 'Stella IT <admin@stella-it.com>'
__copyright__ = 'Copyright 2020, Stella IT'

# Override XML RPC Settings for 64bit support
xmlrpc.client.MAXINT = 2**63-1
xmlrpc.client.MININT = -2**63

app = FastAPI(
    title="Xen API v2",
    description="XenServer Management API to REST API",
    debug=True
)

app.include_router(_v1_router)


class Root:
    terminating = False

    @classmethod
    def main(cls):
        # print banner
        from pyfiglet import Figlet

        figlet = Figlet()

        print(figlet.renderText("XenXenXenSe"))
        print("Project XenXenXenSe : a RESTful API implementation for Citrix Hypervisor® and XCP-ng")
        print()
        print("Copyright (c) Stella IT.")
        print("This software is distributed under Affero GNU Public License v3.")
        print()
        print()
        print("Detected Clusters")
        for credentials in xen_credentials:
            print("*", credentials)

        init_connection()
        print()

        is_dev = (("-d" in sys.argv) or ("--dev" in sys.argv))

        schedule_thread = Thread(target=cls.schedule_process)
        schedule_thread.start()

        if is_dev:
            # development environment
            print("Running in development mode!")
            uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

        else:
            # production environment
            uvicorn.run(app, host="127.0.0.1", port=8000)

        cls.terminating = True
        schedule_thread.join()

    @classmethod
    def schedule_process(cls):
        print("Data Caching Schedule handling has been started!")
        print()
        try:
            while not cls.terminating:
                schedule.run_pending()
                time.sleep(1)
        except:
            cls.terminating = True

        print()
        print("Schedule handling is terminating!")


if __name__ == "__main__":
    root.main()
