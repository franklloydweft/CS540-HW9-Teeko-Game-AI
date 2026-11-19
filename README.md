# CS540 HW9 Spring 2023
This project outlines an AI player of the game [Teeko](https://en.wikipedia.org/wiki/Teeko) and implements the [minimax algorithm](https://www.geeksforgeeks.org/dsa/minimax-algorithm-in-game-theory-set-1-introduction/). I will include the rules of the game as described in the assignment document here:

> It is a game between <mark>two players</mark> on a <mark>5x5 board</mark>. Each player has <mark>four markers</mark> of
either <mark>red</mark> or <mark>black</mark>. <mark>Beginning with black</mark>, they take turns placing markers (the "drop
phase") until all markers are on the board, with <mark>the goal of getting four in a row
horizontally, vertically, or diagonally, or in a 2x2 box as shown above</mark>. If after the drop
phase neither player has won, they continue taking turns <mark>moving one marker at a time --
to an adjacent space only!</mark> *(this includes diagonals, not just left, right, up, and down one
space.)* -- until one player wins. **Note**, the game has no “wrap-around” similar to other
board games, so a player can not move off of the board or win using pieces on the other
side of the board.

## Packages
- `import copy`
- `import random`
- `import numpy as np`

## Functions
- `succ(self, state)`: Takes in a board state (`state`) and returns a list of legal successor states.
- `heuristic_eval(self, state)`: Evaluates non-terminal states to determine behavior without a full search and returns a score between 1 and -1 measuring how optimal that state is in gameplay. What is optimal is determined by the amount of moves from a defined win state.
- `max_value(self, state, drop_phase, depth)`: **Max** value helper function for minimax algorithm implemented in `make_move`. Given the game state, drop phase (are we placing pieces or in play), and current depth returns the **maximized** state and **alpha** value (current guaranteed best value at depth)
- `min_value(self, state, drop_phase, depth)`: **Min** value helper function for minimax algorithm implemented in `make_move`. Given the game state, drop phase (are we placing pieces or in play), and current depth returns the **minimized** state and **beta** value (current guaranteed best value at depth)
- `make_move(self, state)`: Given the current state of the game, `make_move` selects a tuple in the form `(row,col)` representing the next move for the player. Depending on whether the game is in drop phase, the function will output a list of just that tuple or include another tuple in the format `(source_row, source_col)` containing the location where the AI plans to relocate in moves AFTER the drop phase (active gameplay).

The assignment specification stated that my code needed to beat a random player in 2 out of 3 matches, and this code satisfied!
