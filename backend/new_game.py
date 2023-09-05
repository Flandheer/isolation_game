# TODO: implement the __init__ class below by adding properties
# that meet the three requirements specified
import random


class GameState:
    # TODO: The board game now navigates in indices 0,0 ... 6,6 but for human player the interface should be A1,B2, etc.

    def __init__(self, y_length, x_length, player_1, player_2):
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
        self._board = [[False for _ in range(y_length)] for _ in range(x_length)]
        self._player_1 = player_1
        self.position_player_1 = None
        self._player_2 = player_2
        self.position_player_2 = None
        self.last_move = None
        self.game_over = False
        self._active_player = random.choice([self._player_1, self._player_2])

        '''
        Parity: In the context of game theory and artificial intelligence, "parity" refers to a property 
        of certain games that determines whether a player has a winning strategy or not. A game is said to have parity 
        if the outcome of the game is determined solely by the number of moves played, rather than the specific 
        moves themselves. In a game with parity, the player who makes the last move wins if the total number of moves 
        played is odd, and loses if the total number of moves played is even. This means that the player who moves last 
        has an advantage in a game with parity. Parity is an important concept in game theory because it helps determine
        the optimal strategy for a player. By analyzing the parity of a game, we can determine whether a player can 
        force a win or a draw, or if the outcome is uncertain.
        '''

    def has_initiative(self):
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

        if not self.last_move:
            return self._active_player

        elif self.last_move == self._player_1:
            return self._player_2

        else:
            return self._player_1



    def get_all_moves(self):
        """
        Function to retrieve all possible positions on the board
        Returns: List with all possible positions
        """
        return [[x, y] for y in range(len(self._board)) for x in range(len(self._board[0]))]

    def get_all_blanc(self):
        """
        Function to retrieve all blanc spaces on the board
        Returns: List with all possible positions
        """
        return [[x, y] for y in range(len(self._board)) for x in range(len(self._board[0]))
                if self._board[y][x] is False]

    def get_legal_moves(self, position):
        """
        Function to retrieve diagonal moves from a two-dimensional playing board, base ob the position of the player
        Args:
            position:

        Returns: all the possible diagonal moves from the position of the player
        """
        # Length of the board
        board_length = len(self._board)
        # width of the board
        board_width = len(self._board[0])
        # Retrieve the diagonal moves
        legal_moves = []
        # The directions in which the player can move
        directions = [[1, 1], [-1, 1],      # Diagonal  left bottom -> right top
                      [1, -1], [-1, -1],    # Diagonal  left top  -> right bottom
                      [0, 1], [0, -1],      # Horizontal
                      [1, 0], [-1, 0]]      # Vertical

        for direction in directions:
            # Current position is starting point for new position
            new_position = position

            # Check if the new position is within the board and not already occupied
            hit_occupied = False

            while 0 < new_position[0] < board_width and 0 < new_position[1] < board_length and hit_occupied is False:
                # Go through the lines and check if a field is blocked. if not, add it to diagonal moves
                new_position = [new_position[0] + direction[0], new_position[1] + direction[1]]
                if self._board[new_position[0]][new_position[1]] is False:
                    legal_moves.append(new_position)
                else:
                    # This would mean the iteration hit an occupied cell, no further moves in this direction
                    hit_occupied = True

        return legal_moves

    def make_move(self):
        """
        Offers the player the opportunity to make a move. The player is the one that has initiative. The moves is
        restricted. The player only is able to make moves in diagonal, horizontal or vertical lines and can't jump
        over other players, nor locations that are already occupied.
        The board is updated with the new position of the player.

        Returns: The new position of the player, the location as the last move, update the board with the last move,.
        if the move is valid. Otherwise, returns error message,
        if the player can't make any legal move, the game is over.
        """

        # retrieve position of the player. I can improve to say self._active_player.position
        if self._active_player == self._player_1:
            position = self.position_player_1
        else:
            position = self.position_player_2

        if self.position_player_1 is None and self.position_player_2 is None:
            possible_moves = self.get_all_moves()
        else:
            # retrieve the possible moves of the player
            possible_moves = self.get_legal_moves(position)

        if not possible_moves:
            self.game_over = True
            return "Game over"

        give_up = False
        while give_up is False:
            print(f"Please make a move. You can move to the following positions: {possible_moves}")
            move = input()
            move = [int(x) for x in move.split(",")]  # perhaps make moves A1, A2, etc?

            # Check if the move is valid
            if move in possible_moves:
                # Update the board
                self._board[move[0]][move[1]] = True

                # Update the position of the player
                if self._active_player == self._player_1:
                    self.position_player_1 = move
                else:
                    self.position_player_2 = move

                # Update the last move
                self.last_move = move

                # Update the active player
                self._active_player = self.has_initiative()
                return move

            else:
                print("Invalid move, would you like to give up? (y/n)")
                give_it_up = input()
                if give_it_up == "y":
                    give_up = True

        self.game_over = True
        return "Game over"

    def print_board(self):
        """
        Print the board with the current position of the players and the fields that are already occupied:
        X: Player 1
        O: Player 2
        #: Occupied field
         : Empty field
        The board should look like this:
          1 2 3 4 5
        1 # #
        2 # X
        3
        4       O
        5       # #
        """

        pass


if __name__ == "__main__":
    # This code is only executed if "gameagent.py" is the run
    # as a script (i.e., it is not run if "gameagent.py" is
    # imported as a module)
    emptyState = GameState()  # create an instance of the object