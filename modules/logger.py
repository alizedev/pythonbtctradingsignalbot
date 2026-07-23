import logging
import os


class TradingLogger:


    def __init__(self):

        os.makedirs(
            "logs",
            exist_ok=True
        )


        logging.basicConfig(

            filename="logs/trading.log",

            level=logging.INFO,

            format=
            "%(asctime)s | %(levelname)s | %(message)s"

        )


        self.log = logging.getLogger()



    def info(self, message):

        print(
            "INFO:",
            message
        )

        self.log.info(
            message
        )



    def error(self, message):

        print(
            "ERROR:",
            message
        )

        self.log.error(
            message
        )