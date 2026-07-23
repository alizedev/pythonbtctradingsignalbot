import pyqtgraph as pg

from PyQt6 import QtCore, QtGui



class CandlestickItem(pg.GraphicsObject):


    def __init__(self):

        super().__init__()


        self.data = []


        self.picture = QtGui.QPicture()



    # ==========================
    # UPDATE DATA
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

                    "#00ff88"

                )


            else:


                color = QtGui.QColor(

                    "#ff3355"

                )




            pen = QtGui.QPen(

                color

            )


            pen.setWidth(

                2

            )


            painter.setPen(

                pen

            )



            # Wick

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





            # Body

            body_height = abs(

                close - open_price

            )



            if body_height < 1:


                body_height = 1




            rect = QtCore.QRectF(

                index - 0.35,

                min(
                    open_price,
                    close
                ),

                0.7,

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
    # BOUNDS
    # ==========================

    def boundingRect(self):


        if not self.data:


            return QtCore.QRectF()



        lows = [

            c["low"]

            for c in self.data

        ]



        highs = [

            c["high"]

            for c in self.data

        ]



        return QtCore.QRectF(

            0,

            min(lows),

            len(self.data),

            max(highs) - min(lows)

        )