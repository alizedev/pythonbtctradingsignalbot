import pyqtgraph as pg



class CandlestickItem(pg.GraphicsObject):


    def __init__(self):

        super().__init__()

        self.data = []

        self.picture = None



    def setData(self,data):

        self.data=data

        self.generatePicture()

        self.update()



    def generatePicture(self):


        picture = pg.QtGui.QPicture()


        painter = pg.QtGui.QPainter(

            picture

        )



        for index,candle in enumerate(self.data):


            open_price = candle["open"]

            close = candle["close"]

            high = candle["high"]

            low = candle["low"]



            if close >= open_price:

                color="#00ff88"

            else:

                color="#ff3355"



            pen = pg.mkPen(

                color,

                width=2

            )


            painter.setPen(
                pen
            )



            painter.drawLine(

                pg.QtCore.QPointF(
                    index,
                    low
                ),

                pg.QtCore.QPointF(
                    index,
                    high
                )

            )



            painter.drawRect(

                pg.QtCore.QRectF(

                    index-0.3,

                    min(
                        open_price,
                        close
                    ),

                    0.6,

                    max(
                        abs(close-open_price),
                        1
                    )

                )

            )



        painter.end()


        self.picture = picture




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




    def boundingRect(self):

        return pg.QtCore.QRectF(

            0,

            0,

            len(self.data),

            100000

        )