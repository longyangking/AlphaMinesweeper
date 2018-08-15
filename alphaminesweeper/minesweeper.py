'''
Main enigne for Minesweeper
'''
import numpy as np 
from gameutils import MineBoard
from ui import UI

class HumanPlayer:
    def __init__(self, state_shape):
        self.state_shape = state_shape
        self.action = -1

    def play(self, state):
        action = self.action
        self.action = -1
        return action

    def setaction(self, pos):
        Nx, Ny, channel = self.state_shape
        i, j = pos
        self.action = Nx*j + i

class GameEngine:
    def __init__(self, state_shape, player, verbose=False):
        self.state_shape = state_shape
        self.player = player
        self.verbose = verbose

        self.state_shape = state_shape
        self.board_shape = self.state_shape[:2]

        self.mineboard = None
        self.states = list()

    def update_states(self):
        status_board = self.mineboard.get_status_board()
        self.states.append(status_board)

    def get_state(self):
        return self.states[-1]

    def get_board(self):
        return self.mineboard.get_status_board()

    def init(self):
        self.mineboard = MineBoard(board_shape=self.board_shape, verbose=self.verbose)
        self.mineboard.init()
        self.update_states()
        
    def update(self):
        action = self.player.play(self.get_state)
        return self.mineboard.play(action)

class MineSweeper:
    def __init__(self, state_shape, verbose=False):
        self.state_shape = state_shape
        self.verbose =verbose

        self.player = HumanPlayer(self.state_shape)
        self.gameengine = GameEngine(state_shape=self.state_shape, player=self.player, verbose=self.verbose)
        self.gameengine.init()

        self.ui = None

        self.flag = False

    def setaction(self, pos):
        self.player.setaction(pos)
        flag, is_win = self.gameengine.update()
        self.ui.setboard(boardinfo=self.gameengine.get_board())

        if not flag:
            self.ui.gameend(is_win)
        
    def start(self):
        sizeunit = 30
        board = self.gameengine.get_board()

        if self.verbose:
            print("Initiating UI...",end="")

        self.ui = UI(pressaction=self.setaction, boardinfo=board, sizeunit=sizeunit, verbose=self.verbose)
        self.ui.start()

        if self.verbose:
            print("OK!")
        
if __name__=='__main__':
    # Just for debugging
    state_shape = (10,10,1)
    minesweeper = MineSweeper(state_shape,verbose=True)
    minesweeper.start()