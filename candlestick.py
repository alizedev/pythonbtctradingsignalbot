from PyQt6.QtGui import QPicture, QPainter, QPen, QColor
from PyQt6.QtCore import QRectF

import pyqtgraph as pg



class CandlestickItem(pg.GraphicsObject):


    def __init__(self):

        super().__init__()

        self.picture = QPicture()

        self.candles = []

        self.generatePicture()





    def setData(
            self,
            candles
    ):


        self.prepareGeometryChange()


        self.candles = []



        for c in candles:



            if isinstance(c, dict):


                self.candles.append({

                    "time": c["time"],

                    "open": float(c["open"]),

                    "high": float(c["high"]),

                    "low": float(c["low"]),

                    "close": float(c["close"])

                })



            elif isinstance(c, list) and len(c) >= 6:


                self.candles.append({

                    "time": c[0],

                    "open": float(c[1]),

                    "high": float(c[2]),

                    "low": float(c[3]),

                    "close": float(c[4])

                })



        self.generatePicture()

        self.update()







    def generatePicture(
            self
    ):


        self.picture = QPicture()


        painter = QPainter(

            self.picture

        )


        # dünne Candle Breite

        candle_width = 0.25



        for index, candle in enumerate(

                self.candles

        ):



            open_price = candle["open"]

            close_price = candle["close"]

            high = candle["high"]

            low = candle["low"]




            if close_price >= open_price:


                color = QColor(

                    0,

                    200,

                    80

                )


            else:


                color = QColor(

                    220,

                    50,

                    50

                )



            pen = QPen(

                color

            )


            pen.setWidthF(

                1

            )


            painter.setPen(

                pen

            )



            # Wick

            painter.drawLine(

                index,

                low,

                index,

                high

            )



            # Body

            body_height = abs(

                close_price -
                open_price

            )



            if body_height == 0:


                body_height = 0.5





            painter.fillRect(

                QRectF(

                    index - candle_width,

                    min(

                        open_price,

                        close_price

                    ),

                    candle_width * 2,

                    body_height

                ),

                color

            )




        painter.end()







    def paint(
            self,
            painter,
            option,
            widget
    ):


        painter.drawPicture(

            0,

            0,

            self.picture

        )







    def boundingRect(
            self
    ):


        if not self.candles:


            return QRectF()



        lows = [

            c["low"]

            for c in self.candles

        ]



        highs = [

            c["high"]

            for c in self.candles

        ]



        return QRectF(

            0,

            min(lows),

            len(self.candles),

            max(highs) - min(lows)

        )