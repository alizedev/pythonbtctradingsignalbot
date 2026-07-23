import os
import platform
import socket
import time
from datetime import datetime

import config



class DockerModule:
    """
    Docker / Server Monitoring Module

    Funktionen:
    - Docker Erkennung
    - System Status
    - Uptime
    - Health Check
    - Logs
    """


    def __init__(self):

        self.enabled = getattr(
            config,
            "DOCKER_ENABLED",
            True
        )


        self.start_time = time.time()


        if self.enabled:

            print(
                "Docker Module gestartet"
            )



    # =========================
    # DOCKER CHECK
    # =========================


    def is_running_in_docker(self):

        if os.path.exists(
            "/.dockerenv"
        ):

            return True


        return False



    # =========================
    # SYSTEM INFO
    # =========================


    def get_system_info(self):

        return {

            "hostname":
            socket.gethostname(),


            "platform":
            platform.system(),


            "python":
            platform.python_version(),


            "docker":
            self.is_running_in_docker(),


            "time":
            datetime.now()
            .isoformat()

        }



    # =========================
    # UPTIME
    # =========================


    def get_uptime(self):

        seconds = (
            time.time()
            -
            self.start_time
        )


        hours = int(
            seconds // 3600
        )


        minutes = int(
            (
                seconds % 3600
            )
            //
            60
        )


        return {

            "hours":
            hours,

            "minutes":
            minutes

        }



    # =========================
    # HEALTH CHECK
    # =========================


    def health_check(
        self,
        modules=None
    ):


        status = {

            "status":
            "ONLINE",


            "docker":
            self.is_running_in_docker(),


            "uptime":
            self.get_uptime()

        }


        if modules:


            status["modules"] = {}


            for name, module in modules.items():

                try:

                    status["modules"][name] = {

                        "enabled":
                        getattr(
                            module,
                            "enabled",
                            False
                        ),

                        "status":
                        "OK"

                    }


                except Exception:


                    status["modules"][name] = {

                        "status":
                        "ERROR"

                    }


        return status



    # =========================
    # LOGGING
    # =========================


    def write_log(
        self,
        message
    ):


        if not os.path.exists(
            "data/logs"
        ):

            os.makedirs(
                "data/logs"
            )


        file = (
            "data/logs/bot.log"
        )


        with open(
            file,
            "a"
        ) as f:


            f.write(

                f"{datetime.now()} "
                f"{message}\n"

            )



    # =========================
    # SERVER MODE
    # =========================


    def keep_alive(self):

        """
        Wird vom Scheduler genutzt,
        damit der Bot dauerhaft läuft.
        """

        self.write_log(
            "Bot heartbeat"
        )


        return True