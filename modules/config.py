import json
import os


CONFIG_FILE = "binance.json"



DEFAULT_CONFIG = {

    "api_key": "XlV3Jk5eXafEDXwdzO1XoryJ9G46761M4tiOSX6nTydmnbrdb686DULLEW97Y9zxf",

    "api_secret": "Ccb8roL9qg1DTikehsvo1G8nvqmgpzkEh9cLQ4j9PoCx82mA2ZDfUaxOIGn1njP8",

    "symbol": "BTCUSDT",

    "interval": "5m",

    "trade_amount": 50,

    "auto_trade": False

}



def load_config():


    if not os.path.exists(CONFIG_FILE):


        with open(
            CONFIG_FILE,
            "w"
        ) as file:


            json.dump(

                DEFAULT_CONFIG,

                file,

                indent=4

            )


        return DEFAULT_CONFIG



    with open(
        CONFIG_FILE,
        "r"
    ) as file:


        return json.load(file)




def save_config(data):


    with open(
        CONFIG_FILE,
        "w"
    ) as file:


        json.dump(

            data,

            file,

            indent=4

        )