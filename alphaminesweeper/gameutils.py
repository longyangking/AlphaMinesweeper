'''
Game utilities for Minesweeper
'''
import numpy as np

class MineBoard:
    def __init__(self, board_shape, p=0.1, verbose=False):
        self.board_shape = board_shape
        self.p = p

        self.mine_board = None
        self.n_mine_board = None
        self.status_board = None

        self.availables = list()
        self.verbose = verbose

    def init(self):
        if self.verbose:
            print("Initiating Mine Board...", end="")

        #self.mine_board = np.random.randint(2, size=self.board_shape)
        self.mine_board = np.random.choice(2, size=self.board_shape, p=[1-self.p, self.p])
        self.n_mine_board = np.zeros(self.board_shape)

        Nx, Ny = self.board_shape
        # number in corners
        self.n_mine_board[0,0] = self.mine_board[0,1] + self.mine_board[1,0]
        self.n_mine_board[0,Ny-1] = self.mine_board[0,Ny-2] + self.mine_board[1,Ny-1]
        self.n_mine_board[Nx-1,0] = self.mine_board[Nx-2,0] + self.mine_board[Nx-1, 1]
        self.n_mine_board[Nx-1, Ny-1] = self.mine_board[Nx-2, Ny-1] + self.mine_board[Nx-1, Ny-2]
        # number in boundaries
        for i in range(1,Nx-1):
            self.n_mine_board[i, 0] = self.mine_board[i-1,0] + self.mine_board[i+1,0] + self.mine_board[i,1]
            self.n_mine_board[i, Ny-1] = self.mine_board[i-1, Ny-1] + self.mine_board[i+1, Ny-1] + self.mine_board[i-1, Ny-2]
        for j in range(1,Ny-1):
            self.n_mine_board[0,j] = self.mine_board[0,j-1] + self.mine_board[0,j+1] + self.mine_board[1,j]
            self.n_mine_board[Nx-1,j] = self.mine_board[Nx-1,j-1] + self.mine_board[Nx-1,j+1] + self.mine_board[Nx-2,j]
        # number in bulk
        for i in range(1,Nx-1):
            for j in range(1,Ny-1):
                self.n_mine_board[i,j] = self.mine_board[i-1,j] + self.mine_board[i+1,j] + self.mine_board[i,j-1] + self.mine_board[i,j+1]

        # board status:
        #   0~6: the number of surrounding mine
        #    -1: un-explored
        self.status_board = -1*np.ones(self.board_shape)
        self.availables = np.arange(5)

        if self.verbose:
            print("OK!")

    def play(self, action):
        Nx, Ny = self.board_shape
        if (action < 0) or (action >= Nx*Ny):
            return True, False

        pos = (action%Nx, int(action/Nx))

        if self.mine_board[pos] != 0:
            return False, False

        self.__update_status(pos)
        self.__update_availables() 

        if self.__victory_judge():
            return False, True

        return True, False

    def __update_status(self, pos):
        '''
        Update status board recursively
        '''
        self.status_board[pos] = self.n_mine_board[pos]

        Nx, Ny = self.board_shape
        x, y = pos
        if self.status_board[pos] == 0:
            if (x+1 <= Nx-1) and (self.status_board[(x+1,y)] == -1):
                self.__update_status((x+1, y))
            if (x-1 >= 0) and (self.status_board[(x-1,y)] == -1):
                self.__update_status((x-1, y))
            if (y+1 <= Ny-1) and (self.status_board[(x,y+1)] == -1):
                self.__update_status((x, y+1))
            if (y-1 >= 0) and (self.status_board[(x,y-1)] == -1):
                self.__update_status((x, y-1))

    def __update_availables(self):
        '''
        Update available positions
        '''
        Nx, Ny = self.board_shape
        availables = list()
        for i in range(Nx):
            for j in range(Ny):
                if self.status_board[i,j] == -1:
                    availables.append(Nx*j+i)

        self.availables = np.array(availables)

    def __victory_judge(self):
        Nx, Ny = self.board_shape
        for action in self.availables:
            i, j = action%Nx, int(action/Nx)
            if (self.status_board[i,j] == -1) and (self.mine_board[i,j] == 0):
                    return False
        return True

    def get_availables(self):
        return np.copy(self.availables)

    def get_board_shape(self):
        return np.copy(self.board_shape)

    def get_status_board(self):
        return np.copy(self.status_board)