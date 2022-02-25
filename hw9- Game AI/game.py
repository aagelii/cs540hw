import copy
import random


class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    turn = 0

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def succ(self, state, drop_phase, piece):
        moves = []
        if drop_phase:  # not all pieces are placed down
            for r in range(5):
                for c in range(5):
                    if state[r][c] == ' ':  # find empty spaces
                        stateDeepCopy = copy.deepcopy(state)
                        stateDeepCopy[r][c] = piece
                        moves.append(stateDeepCopy)
        else:  # all pieces are placed down
            for r in range(5):
                for c in range(5):
                    if state[r][c] == piece:  # find the successors for the given piece in given spot
                        for x in range(-1, 2):  # checking around the given location's x direction
                            for y in range(-1, 2):  # checking around the given location's x direction
                                if 0 <= r + x < len(state) and 0 <= c + y < len(state[r]) and state[r + x][c + y] == ' ':
                                    stateDeepCopy = copy.deepcopy(state)
                                    stateDeepCopy[r][c] = ' '
                                    stateDeepCopy[r + x][c + y] = piece
                                    moves.append(stateDeepCopy)
        return moves

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
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
        solutionFound = False
        optimal = []
        move = []
        drop_phase = True
        if self.turn >= 4:  # if it's turn 4 or more then it's not drop phase
            drop_phase = False
        else:
            self.turn += 1
        if self.turn == 1:  # first turn to place a piece, just place a random piece
            move.insert(0, (random.randint(0, 4), random.randint(0, 4)))
            return move
        succ = self.succ(state, drop_phase, self.my_piece)
        for i in succ:  # checking for solvability
            gameValue = self.game_value(i)
            if gameValue:  # if there is a state in the successor that can win the game keep it
                optimal = i
                solutionFound = True
                break
        maxValue = -999999  # simulating a negative infinity value to find the best value
        if not solutionFound:  # if solution was not found above
            for i in succ:
                value = self.max_value(i, 0, drop_phase)  # starting depth at 0 as per instruction
                if value > maxValue:  # if a larger value is found keep it
                    maxValue = value
                    optimal = i  # optimal successor with the largest value
        for row in range(5):
            for col in range(5):
                if optimal[row][col] != state[row][col]:  # find where the current state and the optimal differentiate
                    if optimal[row][col] == self.my_piece:  # in drop phase, find where the optimal piece should be played
                        move.insert(0, (row, col))
                    elif not drop_phase and state[row][col] == self.my_piece:
                        move.insert(1, (row, col))
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

    def heuristic_game_value(self, state, piece):
        terminal = self.game_value(state)  # used to check if the state is terminal or not
        heuristic = [[0, 0, 0, 0, 0],  # used for heuristic values best values near center because higher win chance
                     [0, 1, 1, 1, 0],
                     [0, 1, 2, 1, 0],
                     [0, 1, 1, 1, 0],
                     [0, 0, 0, 0, 0]]
        if not terminal:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == piece:  # if piece is found add the heuristic value from above
                        terminal += heuristic[row][col]
        if piece == self.my_piece:  # positive value for your piece, maximizing
            return terminal
        else:
            return -terminal  # negative value for opponent, minimizing

    def max_value(self, state, depth, drop_phase):
        game_value = self.game_value(state)  # obtain game value and check for termination
        if game_value == 1 or game_value == -1:
            return game_value
        elif depth >= 2:  # tried 3 and takes too long, tried 1 and tries too many times, 2 is pretty much perfect
            return self.heuristic_game_value(state, self.my_piece)
        else:
            alpha = -999999  # simulated negative infinity
            succ = self.succ(state, drop_phase, self.my_piece)  # checking successors using bellman equation
            for i in succ:
                alpha = max(alpha, self.min_value(state, depth + 1, drop_phase))
        return alpha

    def min_value(self, state, depth, drop_phase):
        game_value = self.game_value(state)  # obtain game value and check for termination
        if game_value == 1 or game_value == -1:
            return game_value
        elif depth >= 2:  # tried 3 and takes too long, tried 1 and tries too many times, 2 is pretty much perfect
            return self.heuristic_game_value(state, self.opp)
        else:
            beta = 999999  # simulated positive infinity
            succ = self.succ(state, drop_phase, self.opp)  # checking successors using bellman equation
            for i in succ:
                beta = min(beta, self.max_value(state, depth + 1, drop_phase))
        return beta

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 3x3 square corners wins
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

        # TODO: check \ diagonal wins

        for row in range(2):
            for col in range(5):
                if col < 2:
                    if state[row][col] != ' ' and state[row][col] == state[row + 1][col + 1] == state[row + 2][
                        col + 2] == state[row + 3][col + 3]:  # checks down right
                        if state[row][row] == self.my_piece:
                            return 1
                        else:
                            return -1
                else:
                    if state[row][col] != ' ' and state[row][col] == state[row - 1][col - 1] == state[row - 2][
                        col - 2] == state[row - 3][col - 3]:
                        if state[row][row] == self.my_piece:
                            return 1
                        else:
                            return -1
                # there's 2 cases (?) down right and down left, only have to check the first 2 rows
                # only check right for col 0 and 1
                # only check left for col 3 and 4
        # TODO: check / diagonal wins
        # TODO: check 3x3 square corners wins
        for row in range(3):
            for col in range(3):
                if state[row][col] != ' ' and state[row + 2][col] == state[row + 2][col + 2] == state[row][col + 2] == \
                        state[row][col]:
                    if state[row][col] == self.my_piece:
                        return 1
                    else:
                        return -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
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
