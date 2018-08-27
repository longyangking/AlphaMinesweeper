# AlphaMinesweeper
> Play Minesweeper game by Artificial Intelligence

## Features
+ Home-made Minesweeper Game

<img src=./pics/minesweeper.png width="50%" height="50%" />

+ Self-playing reinforcement learning

## Requirements
+ Numpy
+ Keras, Tensorflow
+ h5py
+ PyQt5 (for visualizing) 

## How to use
+ Play MineSweeper Game by yourself
        
        cd alphaminesweeper
        python alphaminesweeper.py --play

+ Re-Train AI model for Minesweeper Game (The model will saved as "model.h5")

        cd alphaminesweeper
        python alphaminesweeper.py --retrain --verbose

+ Continue to train AI model for Minesweeper Game

        cd alphaminesweeper
        python alphaminesweeper.py --train --verbose

+ Visualize AI model to play Minesweeper Game

        cd alphaminesweeper
        python alphaminesweeper.py --playai --verbose

## E-mail
longyang_123@yeah.net  
You're most welcome to contact with me to discuss the details about this project