# TODO: implement the __init__ class below by adding properties
# that meet the three requirements specified
import random
import copy


class GameBoard:

    def __init__(self, x_length, y_length, player_1, player_2):
        """The GameState class constructor performs required
        initializations when an instance is created. The class
        should:

        1) Keep track of which cells are open/closed
        2) Identify which player has initiative
        3) Record the current location of each player

        Parameters
        ----------
        self:
            instance methods automatically take "self" as an
            argument in python

        Returns
        -------
        None
        """

        # Create a board with the same size as the game board
        # and fill it with False values
        self._board_width = x_length
        self._board_height = y_length
        self._board = [[False for _ in range(x_length)] for _ in range(y_length)]
        self.positions = {player_1: None, player_2: None}
        self.game_over = False
        self.player_1 = player_1
        self.player_2 = player_2
        self.active_player = random.choice([self.player_1, self.player_2])

    def change_initiative(self):
        """
        Monitors the player that has initiative. There're three phases:
        1) Game hasn't started yet. The board selects who get's to play first. That's done in the constructor
        2) First move is set by a player. From that moment on, the player interchange moves
        3) Game is over. No one has initiative
        Returns: The player that is active in the self._active_player variable

        INFORMATION BLOCK:
        Has initiative can also be changed with self._active_player ^= 1, if player 1 and 2 would be represented by 0,1
        In Python, the ^ operator is used for the XOR (exclusive OR) operation. XOR returns 1 if the corresponding bits
        are different, and 0 if they are the same. So, self._active_player ^= 1 is flipping the value of _active_player.
         If _active_player is 0, it will become 1, and if _active_player is 1, it will become 0.
        """

        if self.active_player == self.player_1:
            self.active_player = self.player_2
        elif self.active_player == self.player_2:
            self.active_player = self.player_1

    def get_all_blanc(self):
        """
        Function to retrieve all blanc spaces on the board
        Returns: List with all possible positions
        """
        return [[x, y] for x in range(len(self._board[0])) for y in range(len(self._board)) if
                self._board[y][x] is False]

    def get_legal_moves(self, position=None):
        """
        Function to retrieve diagonal moves from a two-dimensional playing board, base ob the position of the player
        Args:
            position:

        Returns: all the possible diagonal moves from the position of the player
        """
        if not position:
            return self.get_all_blanc()
        # width of the board, the first line in [line_1:[F,F,F,F], line_2[F,F,F,F]] is the length (4) of the first line
        x_length = len(self._board[0])

        # Length of the board are the  lines in [line_1:[F,F,F,F], line_2[F,F,F,F]] (2)
        y_length = len(self._board)

        # Retrieve the diagonal moves
        legal_moves = []
        # The directions in which the player can move
        directions = [[1, -1], [-1, 1],  # Diagonal left top  -> right bottom
                      [1, 1], [-1, -1],  # Diagonal left bottom -> right top
                      [0, 1], [0, -1],  # Horizontal
                      [1, 0], [-1, 0]]  # Vertical

        for direction in directions:
            # Current position is starting point for new  position, which is [y,x]
            new_position = position

            # Check if the new position is within the board and not already occupied
            proceed = True
            while proceed:
                # Go through the lines and check if a field is blocked. if not, add it to diagonal moves
                new_position = [new_position[0] + direction[0], new_position[1] + direction[1]]
                # Smaller than, because the board starts at 0 and the lengths are 1 higher
                if not 0 <= new_position[0] < y_length or not 0 <= new_position[1] < x_length:
                    proceed = False

                elif self._board[new_position[0]][new_position[1]] is True:
                    # This would mean the iteration hit an occupied cell, no further moves in this direction
                    proceed = False
                else:
                    legal_moves.append(new_position)

        if len(legal_moves) == 0:
            self.game_over = True

        return legal_moves

    def make_move(self, move):
        """
        Offers the player the opportunity to make a move. The player is the one that has initiative. The moves is
        restricted. The player only is able to make moves in diagonal, horizontal or vertical lines and can't jump
        over other players, nor locations that are already occupied.
        The board is updated with the new position of the player.

        Returns: The new position of the player, the location as the last move, update the board with the last move,.
        if the move is valid. Otherwise, returns error message,
        if the player can't make any legal move, the game is over.
        """

        legal_moves = self.get_legal_moves(self.positions[self.active_player])

        # Make a move on the board at coordinates (x, y)
        if move not in legal_moves:
            return False  # Invalid move

        y = move[0]
        x = move[1]

        self._board[y][x] = True
        self.positions[self.active_player] = move
        self.change_initiative()
        # self.active_player.player_possible_moves = self.get_legal_moves(self.positions[self.active_player])

        # Import to return the board, because the computer player needs to know the board for the iterative deepening
        return self

    def terminal_test(self):
        """
        Game over if no legal moves are left is managed in get_legal_moves. And checked after every move. If player one
        has made the move, it will check if player two has any move left after the move of player one.
        !!! This doesn't account for the fact that player two can block himself and last move player one isn't necessary
        Returns: True if the game is over, otherwise False
        """

        return len(self.get_legal_moves(self.positions[self.active_player])) == 0

    def utility(self):
        """
        The game stop when the active player has no legal moves left. That means that the active player loses.
        If player one has no legal moves, he loses and the score will be -inf. If player two has no legal moves, player
        one wins and the score will be inf.
        Returns: 1 if the player wins, -1 if the player loses, 0 if it's a draw
        """

        # The game stops when the active
        if self.active_player == self.player_1:
            return float("-inf")
        elif self.active_player == self.player_2:
            return float("inf")
        else:
            return 0

    def clone(self):
        """
        Creates a copy of the current board
        :return:
        """

        cloned_board = GameBoard(self._board_width, self._board_height,
                                 self.player_1, self.player_2)
        cloned_board._board = [row[:] for row in self._board]  # Create a deep copy of the board
        cloned_board.game_over = self.game_over
        cloned_board.positions = self.positions.copy()
        cloned_board.active_player = cloned_board.player_1 if self.active_player == self.player_1 else cloned_board.player_2
        cloned_board.player_1 = self.player_1  # Clone player 1
        cloned_board.player_2 = self.player_2  # Clone player 2

        return cloned_board

    def __str__(self):
        """
        Display the current game board with row and column labels.
        """
        x_length = len(self._board[0])
        y_length = len(self._board)

        # Column labels (characters A, B, C, ...)
        column_labels = "    " + "   ".join(chr(65 + i) for i in range(x_length))

        # Create the board representation with row labels and symbols for open and occupied cells
        board_repr = []
        for y in range(y_length):
            row_label = str(y + 1).rjust(2)  # Row labels (numbers 1, 2, 3, ...)
            row = [row_label] + [" T " if self._board[y][x] else " F " for x in range(x_length)]
            board_repr.append(" ".join(row))

        '''
        if self._position_player_1:
            board_repr[self._position_player_1[0]] = board_repr[self._position_player_1[0]].replace(" O ", " 1 ")
        if self._position_player_2:
            board_repr[self._position_player_2[0]] = board_repr[self._position_player_2[0]].replace(" O ", " 2 ")
        '''

        # Combine the column labels and board representation
        board_display = column_labels + "\n" + "\n".join(board_repr)

        return board_display


class Player:

    def __init__(self, player_name, player_type):
        """
        Constructor for the player class
        Args:
            player_name: Name of the player
            player_type: Type of the player (Human or Computer)
        """
        self.player_name = player_name

        # Check if the player_type is valid (either "Human" or "Computer")
        if player_type not in ["Human", "Computer"]:
            raise ValueError("Invalid player_type. Must be 'Human' or 'Computer'.")

        self.player_type = player_type
        self.player_position = None
        self.player_possible_moves = []

    def __str__(self):
        """
        Returns a string representation of the player
        :return:
        """
        return self.player_name + " (" + self.player_type + ")"


class HumanPlayer(Player):
    """ A human player in a game """

    def __init__(self, player_name):
        """
        Constructor for the HumanPlayer class
        Args:
            player_name: Name of the player
        """
        super().__init__(player_name, "Human")

    def human_decision(self, current_state):
        """
        This function asks the user to input a move. The move is checked if it is valid. If not, the user is asked to
        input a new move. Converts a move string to a zero-based index for a game board.

        Parameters:
        move (str): A move string in the format "A1" where the first character represents a column (letter) on the board,
                    and the second character represents a row (number).
        Returns:
        int: A zero-based index corresponding to the column specified in the move.

        Example:
        - For move "A1," convert_move_to_index("A1") returns 0, indicating that "A" maps to column index 0.
        - For move "B2," convert_move_to_index("B2") returns 1, indicating that "B" maps to column index 1.
        :param current_state: The current state of the game
        :return: The move the user has chosen
        """

        # The user has no move yet
        print(f"player position = {current_state.positions[current_state.active_player]}")
        legal_moves = current_state.get_legal_moves(current_state.positions[current_state.active_player])

        # The user is asked to input a move
        move_input = input("Please enter a move (e.g. 'A1'): ")

        # The move is converted to a list of coordinates
        move = [int(move_input[1]) - 1, ord(move_input[0].upper()) - 65]

        print(f'{move_input} -> {move}')
        print(f"These are the legal moves: {legal_moves}")
        if move not in legal_moves:
            print("Invalid move. Please try again.")
            move = self.human_decision(current_state)

        return move


class ComputerPlayer(Player):
    """This subclass of Player representing an AI player. In this class different algortihms are worked out such as
        minimax algorithm with alpha-beta pruning and a depth limited search algorithm."""

    def __init__(self, player_name):
        """
        Constructor for the ComputerPlayer class.
        Args:
            player_name: Name of the player
        """
        super().__init__(player_name, "Computer")

    def my_moves(self, state):
        my_available_moves = state.get_legal_moves(state.positions[state.active_player])

        return len(my_available_moves)

    def get_actions(self, state, min_depth):
        """
        Function to get actions from the minimax_decision function to perform iterative deepening search. It will go
        through a for loop to get the best move for each depth. The best move will be returned.
        :param min_depth: The minimum depth the algorithm should search
        :param state:
        :return:
        """

        best_move_for_depth = None
        for d in range(1, min_depth + 1):
            best_move_for_depth = self.minimax_decision(state, d)

        return best_move_for_depth

    def minimax_decision(self, current_state, depth=float("inf")):
        """
        The gamestate given is a copy of the current gamestate. This function initiates the minimax algorithm with

        This function initiates the minimax algorithm with alpha-beta pruning and returns the best move the player can
        make.
        :return:
        """

        # the computer player has no move yet
        best_move = None
        # The computer player wants to maximize its score, so the best score is set to -inf,
        # you only can go up from the position score
        best_score = float("-inf")

        print(f"player active = {current_state.active_player}")
        print(f"player position = {current_state.positions[current_state.active_player]}")
        legal_moves = current_state.get_legal_moves(current_state.positions[current_state.active_player])
        print(f"These are the legal moves: {legal_moves}")

        # Because the next step is to maximize the score, the computer player will start with the max_value function
        # The max_value function will return the best move and the best score
        for move in current_state.get_legal_moves(current_state.positions[current_state.active_player]):
            new_state = current_state.clone()
            new_value = self.min_value(new_state.make_move(move), depth - 1)
            if new_value > best_score:
                best_score = new_value
                print(f"best score = {best_score}")
                best_move = move

        return best_move

    def min_value(self, state, depth):
        """
        Isolation is a player turn based game. The computer player assumes the human player wants to win, aka the
        computer player to lose. Isolation game is a zerosum game, so in order to let the computer lose, the player will
        choose an move that has lowest effect on progressing the computers game. A move that leads to -inf for the
        computer will lead to a win for the player. Therefor the computer will assume the player will choose that move.
        :return:
        """

        if state.terminal_test():
            return state.utility()

        print(f"Depth = {depth}")
        if depth <= 0:
            return self.my_moves(state)
            # return 0

        value = float("inf")

        # Play out the moves from the new position
        for move in state.get_legal_moves(state.positions[state.active_player]):
            # change the state of the board by making a move. Copy the board state to prevent changing the original
            new_state = state.clone()
            new_value = self.max_value(new_state.make_move(move), depth - 1)
            # Based on the result of the played move, the human player will choose for min result for the computer
            value = min(value, new_value)

        return value

    def max_value(self, state, depth):
        """
        The computer player will choose the move that will lead to the highest score for the computer.
        :return:
        """

        # check if the game is over. If human wins, return -inf, if computer wins, return inf
        if state.terminal_test():
            return state.utility()

        if depth <= 0:
            return self.my_moves(state)
            # return 0

        value = float("-inf")

        # Play out the moves from the new position
        for move in state.get_legal_moves(state.positions[state.active_player]):
            # The move will force the human player to make the next move
            new_state = state.clone()
            new_value = self.min_value(new_state.make_move(move), depth - 1)
            # Based on the result of the played move, the computer player will choose for max result
            value = max(value, new_value)

        return value

    def alpha_beta_search(self, current_state):
        """
        This function initiates the alpha beta pruning search algorithm. The algorithm will start the execution of
        a tree search where for every layer, the alpha or beta value will be found and the other branches will be pruned
        Different from minimax, also because the algorithm start with the max_value function.
        :param current_state:
        :return:
        """

        # the computer player has no move yet
        best_move = None
        # The computer player wants to maximize its score, so the best score is set to -inf,
        # you only can go up from the position score
        best_score = float("-inf")
        alpha = float("-inf")
        beta = float("inf")

        for move in current_state.get_legal_moves(current_state.positions[current_state.active_player]):
            new_state = current_state.clone()
            new_value = self.max_value_alpha_beta(new_state.make_move(move), alpha, beta)
            # alpha = max(alpha, new_value) -> I think this would lead to initiate min_value instead of max_value
            if new_value > best_score:
                best_score = new_value
                best_move = move

        return best_move

    def max_value_alpha_beta(self, state, alpha, beta):
        """
        alpha at every state in the game tree α represents the guaranteed worst-case score that the MAX player could
        achieve.  If the estimate of the upper bound is ever lower than the estimate of the lower bound in any state,
        then the search can be cut off because there are no values between the upper and lower bounds.
        :param state:
        :param alpha:
        :param beta:
        :return:
        """

        if state.terminal_test():
            return state.utility()

        value = float("-inf")

        for move in state.get_legal_moves(state.positions[state.active_player]):
            new_state = state.clone()
            value = max(value, self.min_value_alpha_beta(new_state.make_move(move), alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)

        return value

    def min_value_alpha_beta(self, state, alpha, beta):
        """
        beta at every state in the game tree β represents the guaranteed worst-case score that the MIN player could
        achieve.  If the estimate of the lower bound is ever greater than the estimate of the upper bound in any state,
        then the search can be cut off because there are no values between the upper and lower bounds.
        :param state:
        :param alpha:
        :param beta:
        :return:
        """

        if state.terminal_test():
            return state.utility()

        value = float("inf")

        for move in state.get_legal_moves(state.positions[state.active_player]):
            new_state = state.clone()
            value = min(value, self.max_value_alpha_beta(new_state.make_move(move), alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)


class GameManager:

    def __init__(self):
        """
        Constructor for the GameManager class.
        """
        self.game = None

    def create_game(self):
        """
        Creates a game. Creates a computer player, asks for a human player and initiates the gameBoard,
            game_type: The type of game to be created.
        """
        # The computer player is created
        computer_player = ComputerPlayer("Computer")
        human_player = HumanPlayer("Jantje")

        # The game type is asked
        game_type = input("Please enter the board size: small (2,3), medium (5,5) or standard (6,8)")
        # The game is created
        self.game = GameBoard(2, 3, human_player, computer_player)

    def play_game(self):
        """
        This function plays the game. The game is played until the game is over. The game is over when the terminal
        test is true, meaning a player has no more move left.
        :return:
        """

        # The game is played until the game is over
        while not self.game.terminal_test():
            # The game board is printed
            print(f"\n --- A new round ---\n{self.game}")

            # The current human player is asked to make a move
            if self.game.active_player.player_type == "Human":
                print(f"Your turn player: {self.game.active_player.player_name}!")
                move = self.game.active_player.human_decision(self.game)
            # A move is generated by the computer player
            else:
                print("Computer's turn!")
                move = self.game.active_player.minimax_decision(self.game)

            # The move is made
            print(f"The move is processed in the board")
            self.game.make_move(move)

        print("Game over!")


if __name__ == "__main__":
    print(f"What is : {float('inf') - 1}")
