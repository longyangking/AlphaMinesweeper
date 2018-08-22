'''
Train process for AI model
'''
import numpy as np 
from gameutils import MineBoard
import time
from ai import AI

class SelfplayEngine:
    def __init__(self, ai, verbose):
        self.ai = ai
        self.verbose = verbose

        self.state_shape = ai.get_state_shape()
        self.action_dim = ai.get_action_dim()
        self.board_shape = self.state_shape[:2]

        # training data
        self.states = list()
        self.action_incomes = list()

        self.mineboard = self.mineboard = MineBoard(board_shape=self.board_shape, verbose=self.verbose)
        self.mineboard.init()
        self.update_states()

    def get_state(self):
        return self.states[-1]

    def update_states(self):
        status_board = self.mineboard.get_status_board()
        state = status_board.reshape(self.state_shape)
        self.states.append(state)

    def play_income_virtual(self, action):
        _mineboard = self.mineboard.clone()

        flag, is_win = self.mineboard.play(action)
        income = -1
        if (flag) or ((not flag) and is_win):
            income = 1

        self.mineboard = _mineboard

        return income

    def start(self):

        # First play
        availables = self.mineboard.get_availables()
        action = np.random.choice(availables)
        flag, is_win = self.mineboard.play(action)

        while flag:
            self.update_states()

            action_income = np.zeros(self.action_dim)
            #action, action_income_pred = self.ai.play(self.get_state())
            availables = self.mineboard.get_availables()
            for action in availables:
                action_income[action] = self.play_income_virtual(action)        

            self.action_incomes.append(action_income)

            action = np.argmax(action_income)

            flag, is_win = self.mineboard.play(action)

        # The player will win eventually

        states = np.array(self.states)
        action_incomes = np.array(self.action_incomes)

        return states, action_incomes

class TrainAI:
    def __init__(self, 
        state_shape, 
        action_dim,
        ai=None,
        verbose=False):

        self.state_shape = state_shape
        self.action_dim = action_dim

        self.verbose = verbose

        if ai is not None:
            self.ai = ai
        else:
            self.ai = AI(
                state_shape=state_shape,
                action_dim=action_dim,
                verbose=verbose
            )

        self.losses = list()

    def get_losses(self):
        return np.copy(np.array(self.losses))

    def get_selfplay_data(self, n_round):
        '''
        Run self-play engine and get data
        '''
        if self.verbose:
            starttime = time.time()
            count = 0

        states = list()
        action_incomes = list()

        for i in range(n_round):
            if self.verbose:
                print("Start self-playing to obtain data...(round {0})".format(i+1))

            engine = SelfplayEngine(
                ai=self.ai,
                verbose=self.verbose
            )
            data = engine.start()
            self_states, self_action_incomes = data

            for i in range(len(self_action_incomes)):
                states.append(self_states[i])
                action_incomes.append(self_action_incomes[i])

            count += len(self_action_incomes)
                
        if self.verbose:
            endtime = time.time()
            print("End of self-play: Run Time {0:.2f}s, Set Size: {1}".format(endtime-starttime, count))

        states = np.array(states)
        action_incomes = np.array(action_incomes)

        return states, action_incomes

    def update_ai(self, dataset):
        '''
        Update Network of AI and return Loss
        '''
        if self.verbose:
            starttime = time.time()
            print("Start to update neural network in AI model")

        history = self.ai.train(dataset, epochs=30, batch_size=32)

        if self.verbose:
            endtime = time.time()
            print("End of updating network: Run Time {0:.2f}s".format(endtime-starttime))

        return history.history['loss']

    def start(self, filename):
        '''
        Start to train AI model
        '''

        n_epochs = 1000
        n_round = 100
        n_checkpoint = 100
        
        for i in range(n_epochs):
            if self.verbose:
                print("{0}th training epochs: [selfplay round: {1}] ...".format(i+1, n_round))

            dataset = self.get_selfplay_data(n_round=n_round)
            loss = self.update_ai(dataset)

            self.losses.extend(loss)

            if (i+1)%n_checkpoint == 0:
                if self.verbose:
                    print("Checkpoint: Saving current model in [{0}]".format(filename))
                
                self.ai.save_nnet(filename)

                if self.verbose:
                    print("Checkpoint: End of saving.")