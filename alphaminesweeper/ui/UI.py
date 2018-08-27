import numpy as np 
import threading
from . import nativeUI
from . import viewer

import sys
from PyQt5.QtWidgets import QWidget, QApplication,QDesktopWidget
from PyQt5.QtCore import * 
from PyQt5.QtGui import *

class UI(threading.Thread):
    def __init__(self,pressaction,boardinfo,sizeunit=50,verbose=False):
        threading.Thread.__init__(self)
        self.ui = None
        self.app = None

        self.boardinfo = boardinfo
        self.sizeunit = sizeunit
        self.pressaction = pressaction

        self.verbose = verbose
    
    def run(self):
        self.app = QApplication(sys.argv)
        self.ui = nativeUI.nativeUI(pressaction=self.pressaction,boardinfo=self.boardinfo)
        self.app.exec_()

    def setboard(self,boardinfo):
        while self.ui is None:
            pass
        return self.ui.setboard(boardinfo)
    
    def gameend(self,is_win):
        self.ui.gameend(is_win)

class Viewer(threading.Thread):
    def __init__(self, status_boards, positions, is_win, sizeunit=50,verbose=False):
        threading.Thread.__init__(self)
        self.ui = None
        self.app = None

        self.status_boards = status_boards
        self.positions = positions
        self.is_win = is_win
        
        self.sizeunit = sizeunit

        self.verbose = verbose
    
    def run(self):
        self.app = QApplication(sys.argv)
        self.ui = viewer.Viewer(
            status_boards=self.status_boards, 
            positions=self.positions, 
            is_win=self.is_win,
            sizeunit=self.sizeunit)
        self.app.exec_()