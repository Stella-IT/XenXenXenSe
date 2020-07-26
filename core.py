import os
import json
import sys
import time
import signal
import uvicorn
import schedule

from API.v1 import router as _v1_router
from threading import Thread

# Temp solution
from MySQL import init_connection

class XenXenXenSeCore:
    def __init__(self, app, xen_credentials):
        self.xen_credentials = xen_credentials
        self.terminating = False
        self.app = app

        # include API router
        self.app.include_router(_v1_router)

    @classmethod
    def is_docker(self):
        return "DOCKER_XEN_CREDENTIALS" in os.environ

    @classmethod
    def get_docker_xen_credentials(self):
        return json.loads(os.environ['DOCKER_XEN_CREDENTIALS'])

    @classmethod
    def get_docker_mysql_credentials(self):
        if "DOCKER_MYSQL_CREDENTIALS" in os.environ:
            return json.loads(os.environ['DOCKER_MYSQL_CREDENTIALS'])
        else:
            return None

    @classmethod
    def show_banner(self, add_padding=False):
        """ Show banner for XenXenXenSe Project """
        from pyfiglet import Figlet
        figlet = Figlet()

        print(figlet.renderText("XenXenXenSe"))
        print("Project XenXenXenSe : a RESTful API implementation for Citrix Hypervisor® and XCP-ng")
        print()
        print("Copyright (c) Stella IT.")
        print("This software is distributed under Affero GNU Public License v3.")
        
        if add_padding:
            print()

    def print_xen_hostnames(self, show_title=False):
        """ Print Xen Hostnames to screen """
        if show_title:
            print("Detected Clusters")

        for credentials in self.xen_credentials:
            print("*", credentials)

    def run_api_server(self, development_mode=False):
        """ Run API Server """
        if development_mode:
            # development environment
            print("Running in development mode!")
            uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

        else:
            # production environment
            uvicorn.run(self.app, host="127.0.0.1", port=8000)

    @staticmethod
    def connect_db():
        # Temporary Solution, will refactor to OOP Python. - @zeroday0619 Plz help!
        init_connection()

    def schedule_process(self):
        """ The Thread content to run on scheduler """
        print("Data Caching Schedule handling has been started!")
        print()
        try:
            while not self.terminating:
                schedule.run_pending()
                time.sleep(1)
        except:
            print("Exception was detected")
            self.terminating = True

        print()
        print("Schedule handling is terminating!")

    def start(self):
        self.show_banner(True)
        self.print_xen_hostnames(True)
        print()

        # Detect if server is executed with development mode
        development_mode = (("-d" in sys.argv) or ("--dev" in sys.argv))

        # Create new Thread
        schedule_thread = Thread(target=self.schedule_process)
        schedule_thread.start()

        # Run DB Cache Service
        self.connect_db()

        # Run API Server
        self.run_api_server(development_mode)

        # Termination
        self.terminating = True

        # merge with schedule thread
        schedule_thread.join()
