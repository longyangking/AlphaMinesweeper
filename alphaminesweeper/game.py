'''
Game utilities for Minesweeper
'''
import numpy as np

class MineBoard:
    def __init__(self, board_shape):
        self.board_shape = board_shape

        self.mine_board = np.zeros(self.board)
        self.flag_board = np.ones(self.board)
        self.uncover_board = np.zeros(self.board)

    def init(self):
        # TODO initiate mine board

    def get_board_shape(self):
        return np.copy(self.board_shape)

    def get_mine_board(self):
        return np.copy(self.mine_board)

    def get_flag_board(self):
        return np.copy(self.flag_board)

    def get_uncover_board(self):
        return np.copy(self.uncover_board)