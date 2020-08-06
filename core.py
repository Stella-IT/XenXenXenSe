import os
import ujson
import sys
import time
import signal
import uvicorn
import schedule

from API.v1 import router as _v1_router
from threading import Thread

from config import get_xen_clusters, get_mysql_credentials

# Temp solution
from MySQL import init_connection
from MySQL import DatabaseCore


class XenXenXenSeCore(DatabaseCore):
    def __init__(self, app):
        super().__init__()
        self.manager = self
        self.terminating = False
        self.app = app

        # include API router
        self.app.include_router(_v1_router)

    def database_controller(self):
        @self.app.on_event("startup")
        async def on_startup():
            """database connection"""
            self.manager.metadata.create_all(self.manager.create_engine)
            if not self.manager.database.is_connected:
                await self.manager.database.connect()

        @self.app.on_event("shutdown")
        async def on_shutdown():
            """database disconnection"""
            if self.manager.metadata.is_connected:
                await self.manager.database.disconnect()

    @classmethod
    def is_docker(cls):
        return "DOCKER_XXXS_CONFIG" in os.environ

    @classmethod
    def get_docker_config(cls):
        return ujson.loads(os.environ["DOCKER_XXXS_CONFIG"])

    @classmethod
    def show_banner(cls, add_padding=False):
        """ Show banner for XenXenXenSe Project """
        from pyfiglet import Figlet

        figlet = Figlet()

        print(figlet.renderText("XenXenXenSe"))
        print(
            "Project XenXenXenSe : a RESTful API implementation for Citrix Hypervisor®"
            " and XCP-ng"
        )
        print()
        print("Copyright (c) Stella IT.")
        print("This software is distributed under Affero GNU Public License v3.")

        if add_padding:
            print()

    @staticmethod
    def print_xen_hostnames(show_title=False):
        """ Print Xen Hostnames to screen """
        if show_title:
            print("Detected Clusters")

        for clusters in get_xen_clusters():
            print("*", clusters)

    def run_api_server(self, development_mode=False):
        """ Run API Server """
        if development_mode:
            # development environment

            raise OSError(
                "ERROR: due to edits by @zeroday0619, development mode is deprecated."
                " run reload stuff by YOURSELF."
            )
            # print("Running in development mode!")

            # uvicorn.run("", host="127.0.0.1", port=8000, reload=True)

        else:
            # production environment
            uvicorn.run(self.app, host="127.0.0.1", port=8000)

    def connect_db(self):
        # Temporary Solution, will refactor to OOP Python. - @zeroday0619 Plz help!
        self.database_controller()
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
        development_mode = ("-d" in sys.argv) or ("--dev" in sys.argv)

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
