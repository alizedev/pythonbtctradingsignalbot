import json
import os


class SignalProvider:


    def __init__(self):

        self.file = "signals.json"




    def get_signal(self):


        if not os.path.exists(self.file):

            return None



        try:

            with open(
                self.file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)



        except Exception as e:


            print(
                "Signal Fehler:",
                e
            )


            return None