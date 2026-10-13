import copy
import random
import numpy as np


class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def find_pieces(self, state):
        """
        Searches a current state of the game board for all player pieces and returns a list of indices on the board
        corresponding to each piece. (Helper method for succ)

        :param state: (list of lists) current game state
        :return: (list of tuples) indices of all player pieces of TeekoPlayer object
        """
        my_pieces = []
        for row in range(5):
            for col in range(5):
                if state[row][col] == self.my_piece:
                    this_piece = (row, col)
                    my_pieces.append(this_piece)
        return my_pieces

    def succ(self, state, drop_phase):
        """
        Calculates all valid successor states from a given state and returns them in a list.

        :param state: (list of lists) the given game state
        :param drop_phase: boolean representing the current game phase
        :return: a list of valid successor states for the given state
        """
        succs = []
        if not drop_phase:
            # list of tuples of row and column indices of each player piece
            my_pieces = self.find_pieces(state)
            for piece in my_pieces:
                # left case
                if piece[1] > 0:
                    if state[piece[0]][piece[1] - 1] == ' ':
                        temp_state = copy.deepcopy(state)
                        temp_state[piece[0]][piece[1]] = ' '
                        temp_state[piece[0]][piece[1] - 1] = self.my_piece
                        succs.append(temp_state)
                # right case
                elif piece[1] < 4:
                    if state[piece[0]][piece[1] + 1] == ' ':
                        temp_state = copy.deepcopy(state)
                        temp_state[piece[0]][piece[1]] = ' '
                        temp_state[piece[0]][piece[1] + 1] = self.my_piece
                        succs.append(temp_state)
                # up case
                elif piece[0] > 0:
                    if state[piece[0] - 1][piece[1]] == ' ':
                        temp_state = copy.deepcopy(state)
                        temp_state[piece[0]][piece[1]] = ' '
                        temp_state[piece[0] - 1][piece[1]] = self.my_piece
                        succs.append(temp_state)
                # down case
                elif piece[0] < 4:
                    if state[piece[0] + 1][piece[1]] == ' ':
                        temp_state = copy.deepcopy(state)
                        temp_state[piece[0]][piece[1]] = ' '
                        temp_state[piece[0] + 1][piece[1]] = self.my_piece
                        succs.append(temp_state)
                # diagonal left up
                elif piece[0] > 0 and piece[1] > 0:
                    if state[piece[0] - 1][piece[1] - 1] == ' ':
                        temp_state = copy.deepcopy(state)
                        temp_state[piece[0]][piece[1]] = ' '
                        temp_state[piece[0] - 1][piece[1] - 1] = self.my_piece
                        succs.append(temp_state)
                # diagonal right up
                elif piece[0] > 0 and piece[1] < 4:
                    if state[piece[0] - 1][piece[1] + 1] == ' ':
                        temp_state = copy.deepcopy(state)
                        temp_state[piece[0]][piece[1]] = ' '
                        temp_state[piece[0] - 1][piece[1] + 1] = self.my_piece
                        succs.append(temp_state)
                # diagonal left down
                if piece[0] < 4 and piece[1] > 0:
                    if state[piece[0] + 1][piece[1] - 1] == ' ':
                        temp_state = copy.deepcopy(state)
                        temp_state[piece[0]][piece[1]] = ' '
                        temp_state[piece[0] + 1][piece[1] - 1] = self.my_piece
                        succs.append(temp_state)
                # diagonal right down
                if piece[0] < 4 and piece[1] < 4:
                    if state[piece[0] + 1][piece[1] + 1] == ' ':
                        temp_state = copy.deepcopy(state)
                        temp_state[piece[0]][piece[1]] = ' '
                        temp_state[piece[0] + 1][piece[1] + 1] = self.my_piece
                        succs.append(temp_state)
        else:
            for row in range(5):
                for col in range(5):
                    if state[row][col] != ' ':
                        temp = copy.deepcopy(state)
                        temp[row][col] = self.my_piece
                        succs.append(temp)

        return succs

    def heuristic_eval(self, state):
        """
        Heuristic function to analyze how optimal a given game state is. Returns a representative score.
        Measures optimality by counting adjacent pieces corresponding to each goal state. More negative scores indicate
        the opponent is maximized, more positive scores indicate that the TeekoPlayer is maximized.

        :param state:  (list of lists) the given game state
        :return: A score between 1 and -1 indicating the optimality of a game state
        """
        if self.game_value(state) == 1:
            # goal state: this player wins
            return 1
        elif self.game_value(state) == -1:
            # worst case state: opponent wins
            return -1

        max_opp = 0
        max_self = 0
        count_self = 0
        count_opp = 0

        # horizontal case
        for row in range(5):
            for col in range(5):
                if state[row][col] == self.my_piece:
                    count_self += 1
                if count_self > max_self:
                    max_self = count_self
                max_self = 0

        for row in range(5):
            for col in range(5):
                if state[row][col] == self.opp:
                    count_opp += 1
                if count_opp > max_opp:
                    max_opp = count_self
                max_opp = 0

        # vertical case
        for row in range(5):
            for col in range(5):
                if state[col][row] == self.my_piece:
                    count_self += 1
                if count_self > max_self:
                    max_self = count_self
                max_self = 0

        for row in range(5):
            for col in range(5):
                if state[col][row] == self.opp:
                    count_opp += 1
                if count_opp > max_opp:
                    max_opp = count_self
                max_opp = 0

        # right diagonal case
        count_self = 0
        count_opp = 0

        for row in range(3, 5):
            for i in range(2):
                if state[row][i] == self.my_piece:
                    count_self += 1
                if state[row - 1][i + 1] == self.my_piece:
                    count_self += 1
                if state[row - 2][i + 2] == self.my_piece:
                    count_self += 1
                if state[row - 3][i + 3] == self.my_piece:
                    count_self += 1

                if count_self > max_self:
                    max_self = count_self
                count_self = 0

        for row in range(3, 5):
            for i in range(2):
                if state[row][i] == self.opp:
                    count_opp += 1
                if state[row - 1][i + 1] == self.opp:
                    count_opp += 1
                if state[row - 2][i + 2] == self.opp:
                    count_opp += 1
                if state[row - 3][i + 3] == self.opp:
                    count_opp += 1
                if count_opp > max_opp:
                    max_opp = count_opp
                count_opp = 0

        # left diagonal case
        count_self = 0
        count_opp = 0

        for row in range(2):
            for i in range(2):
                if state[row][i] == self.my_piece:
                    count_self += 1
                if state[row + 1][i + 1] == self.my_piece:
                    count_self += 1
                if state[row + 2][i + 2] == self.my_piece:
                    count_self += 1
                if state[row + 3][i + 3] == self.my_piece:
                    count_self += 1
                if count_self > max_self:
                    max_self = count_self
                count_self = 0

        for row in range(2):
            for i in range(2):
                if state[row][i] == self.opp:
                    count_opp += 1
                if state[row + 1][i + 1] == self.opp:
                    count_opp += 1
                if state[row + 2][i + 2] == self.opp:
                    count_opp += 1
                if state[row + 3][i + 3] == self.opp:
                    count_opp += 1
                if count_opp > max_opp:
                    max_opp = count_opp
                count_opp = 0

        # square case
        count_self = 0
        count_opp = 0

        for row in range(4):
            for i in range(4):
                if state[row][i] == self.my_piece:
                    count_self += 1
                if state[row][i + 1] == self.my_piece:
                    count_self += 1
                if state[row + 1][i] == self.my_piece:
                    count_self += 1
                if state[row + 1][i + 1] == self.my_piece:
                    count_self += 1
                if count_self > max_self:
                    max_self = count_self
                count_self = 0

        for row in range(4):
            for i in range(4):
                if state[row][i] == self.opp:
                    count_opp += 1
                if state[row][i + 1] == self.opp:
                    count_opp += 1
                if state[row + 1][i] == self.opp:
                    count_opp += 1
                if state[row + 1][i + 1] == self.opp:
                    count_opp += 1
                if count_opp > max_opp:
                    max_opp = count_opp
                count_opp = 0

        if max_self == max_opp:
            return 0, state
        if max_self >= max_opp:
            return max_self / 6, state  # more adjacent pieces for self

        return -1 * (max_opp / 6), state  # more adjacent pieces for opponent

    def max_value(self, state, drop_phase, depth):
        """
        Max value helper function for the minimax algorithm

        :param state: a game state
        :param drop_phase: the current status of the game drop phase
        :param depth: search depth limit
        :return: the maximized state and alpha value
        """
        cur_state = state
        if self.game_value(state) != 0:
            return self.game_value(state), state
        if depth >= 3:
            return self.heuristic_eval(state)
        else:
            alpha = float('-Inf')
            for s in self.succ(state, drop_phase):
                val = self.min_value(s, drop_phase, depth + 1)
                if val[0] > alpha:
                    alpha = val[0]
                    cur_state = s
        return alpha, cur_state

    def min_value(self, state, drop_phase, depth):
        """
        Min value helper function for minimax algorithm

        :param state: a game state
        :param drop_phase: the current status of game drop phase
        :param depth: search depth limit
        :return: the minimized state and beta value
        """
        cur_state = state
        if self.game_value(state) != 0:
            return self.game_value(state), state
        if depth >= 3:
            return self.heuristic_eval(state)
        else:
            beta = float('Inf')
            for s in self.succ(state, drop_phase):
                val = self.max_value(s, drop_phase, depth + 1)
                if val[0] < beta:
                    beta = val[0]
                    cur_state = s
        return beta, cur_state

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = True

        # detect end of drop phase
        num_black = 0
        num_red = 0
        for i in state:
            num_black += i.count('b')
            num_red += i.count('r')
        num_total = num_black + num_red
        if num_total == 8:
            drop_phase = False

        move = []
        ''' RANDOM CHOICE
        (row, col) = (random.randint(0, 4), random.randint(0, 4))
        while not state[row][col] == ' ':
            (row, col) = (random.randint(0, 4), random.randint(0, 4))
        '''
        if not drop_phase:
            # choose and move piece
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            score, new_state = self.max_value(state, drop_phase, 0)
            diffs = np.equal(state, new_state)
            indices = np.where(diffs == False)
            #handles empty case
            if state[[indices[0][0]][indices[1][0]]] == ' ':
                new = (indices[0][0], indices[1][0])
                original = (indices[0][1], indices[1][1])
            else:
                new = (indices[0][1], indices[1][1])
                original = (indices[0][0], indices[1][0])
            move.insert(0, new)
            move.insert(1, original)
            return move

        # ensure the destination (row,col) tuple is at the beginning of the move list
        score, new_state = self.max_value(state, drop_phase, 0)
        diffs = np.equal(state, new_state)
        indices = np.where(diffs == False)
        new = (indices[0][0], indices[1][0])
        # handles empty board case
        while not state[new[0]][new[1]] == ' ':
            new = (indices[0][0], indices[1][0])
        move.insert(0, new)
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][
                    col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # check \ diagonal wins
        for row in range(5):
            for col in range(5):
                if row <= 1 and col <= 1:
                    if state[row][col] != ' ' and state[row][col] == state[row + 1][col + 1] == state[row + 2][
                        col + 2] == state[row + 3][col + 3]:
                        return 1 if state[row][col] == self.my_piece else -1

        # check / diagonal wins
        for row in range(5):
            for col in range(5):
                if row >= 3 and col <= 1:
                    if state[row][col] != ' ' and state[row][col] == state[row - 1][col + 1] == state[row - 2][
                        col + 2] == state[row - 3][col + 3]:
                        return 1 if state[row][col] == self.my_piece else -1

        # check box wins
        for row in range(5):
            for col in range(5):
                if row <= 3 and col <= 3:
                    if state[row][col] != ' ' and state[row][col] == state[row + 1][col] == state[row + 1][col + 1] == \
                            state[row][col + 1]:
                        return 1 if state[row][col] == self.my_piece else -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
