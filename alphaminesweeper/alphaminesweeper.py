'''
Main process for AlphaMineSweeper
'''
import numpy as np 
import argparse

__version__ = "0.0.1"
__author__ = "Yang Long"
__info__ = "Play Minesweeper Game with AI"

__default_board_shape__ = 9, 9
__default_state_shape__ = *__default_board_shape__, 1
__filename__ = 'model.h5'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__info__)
    parser.add_argument("--retrain", action='store_true', default=False, help="Re-Train AI")
    parser.add_argument("--train",  action='store_true', default=False, help="Train AI")
    parser.add_argument("--verbose", action='store_true', default=False, help="Verbose")
    parser.add_argument("--play", action='store_true', default=False, help="Play game")
    parser.add_argument("--playai", action='store_true', default=False, help="Play game with AI")

    args = parser.parse_args()
    verbose = args.verbose

    if args.train:
        if verbose:
            print("Start to train AI")

        # TODO Load lastest model here and continue training

    if args.retrain:
        if verbose:
            print("Start to re-train AI with state shape: {0}".format(__default_state_shape__))

        from train import TrainAI

        trainai = TrainAI(
            state_shape=__default_state_shape__,
            verbose=verbose
        )
        trainai.start(__filename__)

    if args.playai:
        from ai import AI
        from sudoku import Sudoku

        ai = AI(state_shape=__default_state_shape__, verbose=verbose)
        ai.load_nnet(__filename__)

        if verbose:
            print("AI player has been initiated from file: {0}".format(__filename__))

        sudoku = Sudoku(state_shape=__default_state_shape__, player=ai, verbose=verbose)
        sudoku.ai_start()

    if args.play:
        print("Play game. Please close game in terminal after closing window (i.e, Press Ctrl+C).")
        from sudoku import Sudoku

        sudoku = Sudoku(state_shape=__default_state_shape__, player=None, verbose=verbose)
        sudoku.start()