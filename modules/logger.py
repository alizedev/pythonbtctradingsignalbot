from datetime import datetime



class TradingLogger:


    def __init__(self):

        pass





    # ==========================
    # INFO
    # ==========================

    def info(

        self,

        message

    ):


        text = (

            f"[{self.time()}] INFO: {message}"

        )


        print(text)


        return text






    # ==========================
    # ERROR
    # ==========================

    def error(

        self,

        message

    ):


        text = (

            f"[{self.time()}] ERROR: {message}"

        )


        print(text)


        return text






    # ==========================
    # WARNING
    # ==========================

    def warning(

        self,

        message

    ):


        text = (

            f"[{self.time()}] WARNING: {message}"

        )


        print(text)


        return text






    # ==========================
    # TIME
    # ==========================

    def time(self):


        return datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        )