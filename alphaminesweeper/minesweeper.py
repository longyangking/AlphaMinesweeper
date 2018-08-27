'''
Main enigne for Minesweeper
'''
import numpy as np 
from gameutils import MineBoard
from ui import UI, Viewer

class HumanPlayer:
    def __init__(self, state_shape):
        self.state_shape = state_shape
        self.action = -1

    def play(self, state):
        action = self.action
        self.action = -1
        return action, None

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
        state = status_board.reshape(self.state_shape)
        self.states.append(state)

    def get_state(self):
        return self.states[-1]

    def get_board(self):
        return self.mineboard.get_status_board()

    def init(self):
        self.mineboard = MineBoard(board_shape=self.board_shape, verbose=self.verbose)
        self.mineboard.init()
        self.update_states()
        
    def update(self, is_ai=False):
        action, _action_incomes = self.player.play(self.get_state())
        if is_ai:
            availables = self.mineboard.get_availables()
            action_incomes = -1*np.ones(_action_incomes.shape)
            action_incomes[availables] = _action_incomes[availables]
            action = np.argmax(action_incomes)
        flag, is_win = self.mineboard.play(action)
        return flag, is_win, action

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
        flag, is_win, action = self.gameengine.update()
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

class VisualizeAI:
    def __init__(self, state_shape, ai, verbose):
        self.state_shape = state_shape
        self.ai = ai
        self.verbose = verbose

        self.status_boards = list()
        self.positions = list()

    def start(self):
        if self.verbose:
            print("Running a new game for AI ...")

        Nx, Ny, channel = self.state_shape
        gameengine = GameEngine(state_shape=self.state_shape, player=self.ai, verbose=self.verbose)
        gameengine.init()

        self.status_boards.append(gameengine.get_board())
        flag, is_win, action = gameengine.update(is_ai=True)
        position = (action%Nx, int(action/Nx))
        self.positions.append(position)

        while flag:
            self.status_boards.append(gameengine.get_board())
            flag, is_win, action = gameengine.update(is_ai=True)
            position = (action%Nx, int(action/Nx))
            self.positions.append(position)

        self.status_boards.append(gameengine.get_board())

        if self.verbose:
            print("End of game with steps [{0}]. Start to visualize ...".format(len(self.positions)))

        ui = Viewer(
            status_boards=self.status_boards, 
            positions=self.positions, 
            is_win=is_win)

        ui.start()
        
if __name__=='__main__':
    # Just for debugging
    state_shape = (10,10,1)
    minesweeper = MineSweeper(state_shape,verbose=True)
    minesweeper.start()