from PyQt6 import QtCore, QtGui

import pyqtgraph as pg




class CandlestickItem(pg.GraphicsObject):


    def __init__(self):

        super().__init__()

        self.data = []

        self.picture = QtGui.QPicture()



    # ==========================
    # UPDATE
    # ==========================

    def setData(self, data):

        self.data = data

        self.generatePicture()

        self.prepareGeometryChange()

        self.update()



    # ==========================
    # DRAW CANDLES
    # ==========================

    def generatePicture(self):


        self.picture = QtGui.QPicture()


        painter = QtGui.QPainter(

            self.picture

        )



        for index, candle in enumerate(self.data):


            open_price = candle["open"]

            close = candle["close"]

            high = candle["high"]

            low = candle["low"]



            if close >= open_price:

                color = QtGui.QColor(
                    "#00e676"
                )


            else:

                color = QtGui.QColor(
                    "#ff5252"
                )



            painter.setPen(

                QtGui.QPen(

                    color,

                    0.7

                )

            )



            # Wick (dünn)

            painter.drawLine(

                QtCore.QPointF(

                    index,

                    low

                ),

                QtCore.QPointF(

                    index,

                    high

                )

            )



            # Candle Body schmal

            body_width = 0.25


            body_height = abs(

                close - open_price

            )


            if body_height < 1:

                body_height = 1



            rect = QtCore.QRectF(

                index - body_width / 2,

                min(
                    open_price,
                    close
                ),

                body_width,

                body_height

            )



            painter.drawRect(

                rect

            )



        painter.end()




    # ==========================
    # PAINT
    # ==========================

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




    # ==========================
    # BOUNDING BOX
    # ==========================

    def boundingRect(self):


        if not self.data:


            return QtCore.QRectF()



        lows = [

            candle["low"]

            for candle in self.data

        ]



        highs = [

            candle["high"]

            for candle in self.data

        ]



        return QtCore.QRectF(

            0,

            min(lows),

            len(self.data),

            max(highs) - min(lows)

        )