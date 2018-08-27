'''
Main process for AlphaMineSweeper
'''
import numpy as np 
import argparse

__version__ = "0.0.1"
__author__ = "Yang Long"
__info__ = "Play Minesweeper Game with AI"

__default_board_shape__ = 10, 10
__default_state_shape__ = *__default_board_shape__, 1
__default_action_dim__ = 100
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
            print("Continue to train AI with state shape: {0}".format(__default_state_shape__))

        from ai import AI
        from train import TrainAI

        ai = AI(
                state_shape=__default_state_shape__,
                action_dim=__default_action_dim__,
                verbose=verbose
            )

        if verbose:
            print("Load AI model from file: [{0}] ...".format(__filename__),end="")

        ai.load_nnet(__filename__)

        if verbose:
            print("OK!")
        

        trainai = TrainAI(
            state_shape=__default_state_shape__, 
            action_dim=__default_action_dim__,
            ai=ai,
            verbose=verbose
        )
        trainai.start(__filename__)
        
        if verbose:
            print("Trained AI model is saved as: [{0}]".format(__filename__))

    if args.retrain:
        if verbose:
            print("Start to re-train AI with state shape: {0}".format(__default_state_shape__))

        from train import TrainAI

        trainai = TrainAI(
            state_shape=__default_state_shape__, 
            action_dim=__default_action_dim__,
            verbose=verbose
        )
        trainai.start(__filename__)

        if verbose:
            print("Re-trained AI model is saved as: [{0}]".format(__filename__))

    if args.playai:
        if verbose:
            print("Visualize Minesweeper with AI [state shape: {0}]".format(__default_state_shape__))

        from ai import AI
        from minesweeper import VisualizeAI

        ai = AI(
                state_shape=__default_state_shape__,
                action_dim=__default_action_dim__,
                verbose=verbose
            )
        if verbose:
            print("Load AI model from file: [{0}] ...".format(__filename__),end="")

        ai.load_nnet(__filename__)
        if verbose:
            print("OK!")

        vi = VisualizeAI(
            state_shape=__default_state_shape__,
            ai=ai,
            verbose=verbose
        )

        vi.start()

    if args.play:
        print("Play game. Please close game in terminal after closing window (i.e, Press Ctrl+C).")
        from minesweeper import MineSweeper

        minesweeper = MineSweeper(state_shape=__default_state_shape__,verbose=verbose)
        minesweeper.start()