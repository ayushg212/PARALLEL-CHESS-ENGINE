# Parallel Chess Engine with Pygame

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Game Modes](#game-modes)
- [Computer Move Generation](#computer-move-generation)
- [Acknowledgements](#acknowledgements)

## Introduction
This is a chess application built using Python and Pygame. It features both multiplayer mode and a mode to play against the computer. The application includes various functionalities to enhance the user experience, such as move highlighting, undo move, and more.
![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image.png) |![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-1.png)
:-------------------------:|:-------------------------:
![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-2.png)|![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-10.png)

## Features
1. **Piece Move Highlighting**: Highlights all possible moves for a selected piece.

![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-3.png) |  ![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-12.png)
:-------------------------:|:-------------------------:
3. **Last Move Highlighting**: Highlights the last move made on the board.

![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-13.png) |  ![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-14.png)
:-------------------------:|:-------------------------:
4. **Pawn Promotion**: Automatically prompts for pawn promotion when a pawn reaches the last rank.

![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-5.png)|  ![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-6.png)
:-------------------------:|:-------------------------:
5. **Mouse Hover Highlighting**: Highlights the square under the mouse cursor.
6. **Undo Move**: Press 'Z' to undo the last move.
7. **Check Highlighting**: Highlights the king's square when in check.

![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-4.png)|  ![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-15.png)
:-------------------------:|:-------------------------:
8. **Board Reset**: Press 'R' to reset the board to the initial position.
9. **Castling**: Supports castling for both kingside and queenside.

![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-7.png)|  ![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-8.png)
:-------------------------:|:-------------------------:
10. **En Passant**: Implements the en passant rule.

![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-9.png)|  ![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-16.png)
:-------------------------:|:-------------------------:

## Installation
1. **Clone the repository**
    ```sh
    git clone https://github.com/ayushg212/PARALLEL-CHESS-ENGINE.git
    cd PARALLEL-CHESS-ENGINE
    ```
2. **Install the dependencies**
    ```sh
    pip install -r requirements.txt
    ```

## Usage
To start the application, run the following command:
```sh
python chessUIandMainFIle.py.
```
## Game Modes
1. **Multiplayer Mode**: Allows two players to play against each other on the same device.
2. **Play with Computer**: Play against an AI that uses the Minimax algorithm with optimizations like Alpha-Beta Pruning, Move Ordering, Beam Search, and Parallel Processing.

## Computer Move Generation
The computer moves are generated using the Minimax algorithm, enhanced with the following techniques:

1. **Alpha-Beta Pruning**: Reduces the number of nodes evaluated by the Minimax algorithm.
2. **Move Ordering**: Improves the efficiency of Alpha-Beta Pruning by evaluating the best moves first.
3. **Beam Search**: Limits the number of moves considered at each depth level to optimize performance.
4. **Parallel Processing**: Utilizes the multiprocessing library to evaluate moves in parallel, speeding up the computation.
   
## Acknowledgements
Thanks to the Pygame community for providing an easy-to-use framework for game development.




![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-4.png)
![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-5.png)
![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-6.png)
![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-7.png)
![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-8.png)
![alt text](https://github.com/ayushg212/PARALLEL-CHESS-ENGINE/blob/main/Screenshots/image-9.png)




