import numpy as np 
import sys
from PyQt5.QtWidgets import QWidget, QApplication,QDesktopWidget
from PyQt5.QtCore import * 
from PyQt5.QtGui import *

class nativeUI(QWidget):
    playsignal = pyqtSignal(tuple) 

    def __init__(self,pressaction,boardinfo,sizeunit=50):
        super(nativeUI,self).__init__(None)
        self.boardinfo = boardinfo
        self.sizeunit = sizeunit

        self.mousex = 0
        self.mousey = 0

        self.chooseX = 0
        self.chooseY = 0
        self.playstatus = False

        self.isgameend = False
        self.is_win = False

        self.pressaction = pressaction

        self.playsignal.connect(self.pressaction) 
        self.initUI()

    def getboardinfo(self):
        return self.boardinfo

    def setboard(self,boardinfo):
        self.boardinfo = boardinfo
        self.update()

    def initUI(self):
        (Nx,Ny) = self.boardinfo.shape
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()

        self.setGeometry((screen.width()-size.width())/2, 
                        (screen.height()-size.height())/2,
                        Nx*self.sizeunit, Ny*self.sizeunit)
        self.setWindowTitle("MineSweeper")
        self.setWindowIcon(QIcon('./ui/icon.png'))

        # set Background color
        palette =  QPalette()
        palette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(palette)

        self.setMouseTracking(True)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawmines(qp)
        self.drawboard(qp)
        self.chooseblock(qp)
        if self.isgameend:
            self.drawgameend(qp)
        qp.end()

    def gameend(self, is_win):
        self.isgameend = True
        self.is_win = is_win

    def drawgameend(self,qp):
        if self.is_win:
            s_win = "Win"
        else:
            s_win = "Fail"

        size =  self.geometry()
        qp.setPen(0)
        qp.setBrush(QColor(200, 200, 200, 180))
        width = size.width()/5*4
        height = size.height()/3
        qp.drawRect(size.width()/2-width/2, size.height()/2-height/2, width, height)

        qp.setPen(QColor(0,0,0))
        font = qp.font()
        font.setPixelSize(60)
        qp.setFont(font)
        qp.drawText(QRect(size.width()/2-width/2, size.height()/2-height/2, width, height),	0x0004|0x0080,str(s_win))

    def mouseMoveEvent(self,e):
        self.mousex = int(e.x()/self.sizeunit)
        self.mousey = int(e.y()/self.sizeunit)
        self.update() 
    
    def mousePressEvent(self,e):
        X = int(e.x()/self.sizeunit)
        Y = int(e.y()/self.sizeunit)
        if (self.boardinfo[X,Y] == -1):
            self.chooseX = X
            self.chooseY = Y
            self.playsignal.emit((X,Y))
            self.update()

    def chooseblock(self,qp):
        #qp.setBrush(QColor(0, 0, 0))
        qp.setPen(QColor(255, 0, 0))
        qp.setBrush(QBrush(Qt.Dense6Pattern))
        x = y = self.sizeunit/10
        dx = dy = self.sizeunit*(1-2/10)
        qp.drawRect(self.mousex*self.sizeunit + x, self.mousey*self.sizeunit + y, dx, dy)

    def drawboard(self,qp):
        (Nx,Ny) = self.boardinfo.shape
        qp.setPen(QColor(0, 0, 0))
        for i in range(Nx):
            qp.drawLine(i*self.sizeunit, 0, i*self.sizeunit, Ny*self.sizeunit)   
        for j in range(Ny):
            qp.drawLine(0, j*self.sizeunit, Ny*self.sizeunit, j*self.sizeunit) 

    def drawmines(self, qp):
        (Nx,Ny) = self.boardinfo.shape
        qp.setPen(0)
        for i in range(Nx):
            for j in range(Ny):
                if self.boardinfo[i,j] == -1:
                    qp.setBrush(QColor(99, 148, 199))
                    qp.drawRect(i*self.sizeunit, j*self.sizeunit, self.sizeunit, self.sizeunit)
                else:
                    qp.setPen(QColor(255,0,0))
                    qrect = QRect(i*self.sizeunit, j*self.sizeunit, self.sizeunit, self.sizeunit)
                    if self.boardinfo[i,j] != 0:
                        qp.drawText(qrect, 0x0004|0x0080, str(int(self.boardinfo[i,j])))
                # qp.setPen(QColor(0,0,0))
                # qrect = QRect(i*self.sizeunit, j*self.sizeunit, self.sizeunit, self.sizeunit)
                # if self.boardinfo[i,j] != 0:
                #     qp.drawText(qrect, 0x0004|0x0080, str(int(self.boardinfo[i,j])))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    boardinfo = -1*np.ones((10,10))
    boardinfo[1,2] = 1
    boardinfo[5,5] = 0
    sizeunit = 50
    ex = nativeUI(pressaction=lambda x:x,boardinfo=boardinfo,sizeunit=sizeunit)
    sys.exit(app.exec_())

