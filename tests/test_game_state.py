import unittest
from backend.new_game import *


class TestGameState(unittest.TestCase):

    def test_game_state(self):
        pass

    def test_init(self):
        """ Test the initialization of the game state"""
        pass

    def test_small_game_over(self):
        """ Test the initialization of the game state"""
        human_player1 = HumanPlayer("Frank")
        human_player2 = HumanPlayer("Jantje")
        self.game_state = GameBoard(3, 2, human_player1, human_player2)
        self.game_state.active_player = human_player1
        moves = [[0, 0], [1, 0], [0, 1], [1, 1], [0, 2], [1, 2]]
        final_move = None
        for move in moves:
            self.game_state.make_move(move)
            if self.game_state.terminal_test():
                final_move = move
                break

        self.assertEqual(final_move, [1, 2])

    def test_medium_game_over(self):
        """ Test the initialization of the game state"""
        human_player1 = HumanPlayer("Frank")
        human_player2 = HumanPlayer("Jantje")
        self.game_state = GameBoard(5, 5, human_player1, human_player2)
        self.game_state.active_player = human_player1
        moves = [[2, 2], [4, 4], [3, 2], [3, 3], [4, 2], [0, 3], [2, 0], [0, 0], [2, 1],
                 [1, 1], [1, 2], [2, 1], [1, 3], [0, 1], [2, 3], [1, 0], [2, 4]]
        final_move = None
        for move in moves:
            self.game_state.make_move(move)
            if self.game_state.terminal_test():
                final_move = move
                break

        self.assertEqual(final_move, [2, 4])

    def test_legal_moves_small_board(self):
        """ Fill a small board with a few moves and check if the legal moves are correct"""

        self.game_state = GameBoard(3, 2, "test_pl_1", "test_pl_2")
        self.game_state._active_player = self.game_state.player_1
        self.game_state.position_player_1 = [1, 1]
        occupied_positions = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2]]
        for position in occupied_positions:
            y = position[0]
            x = position[1]
            self.game_state._board[y][x] = True

        self.assertEqual(self.game_state.get_legal_moves(self.game_state.position_player_1), [[0, 2]])

    def test_legal_moves_medium_board(self):
        """ Fill a medium board with a few moves and check if the legal moves are correct"""

        self.game_state = GameBoard(5, 5, "test_pl_1", "test_pl_2")
        self.game_state._active_player = self.game_state.player_1
        self.game_state.position_player_1 = [3, 1]
        occupied_positions = [[1, 1], [1, 2], [1, 3], [2, 3], [3, 3], [3, 4]]
        for position in occupied_positions:
            y = position[0]
            x = position[1]
            self.game_state._board[y][x] = True

        # Create a list of possible moves and sort it and run the test and sort the result
        possible_moves = sorted([[2, 0], [2, 1], [2, 2], [3, 0], [3, 2], [4, 0], [4, 1], [4, 2]])
        self.assertEqual(sorted(self.game_state.get_legal_moves(self.game_state.position_player_1)), possible_moves)

    def test_legal_moves_large_board(self):
        """ Fill a large board with a few moves and check if the legal moves are correct"""

        self.game_state = GameBoard(8, 6, "test_pl_1", "test_pl_2")
        self.game_state._active_player = self.game_state.player_1
        self.game_state.position_player_1 = [3, 3]
        occupied_positions = [[3, 3], [4, 2], [4, 3], [5, 3], [5, 4], [4, 5], [4, 6], [3, 6], [2, 5]]
        for position in occupied_positions:
            y = position[0]
            x = position[1]
            self.game_state._board[y][x] = True

        # Create a list of possible moves and sort it and run the test and sort the result
        possible_moves = sorted([[0, 0], [0, 3], [0, 6], [1, 1], [1, 3], [1, 5], [2, 2], [2, 3], [2, 4],
                                 [3, 0], [3, 1], [3, 2], [3, 4], [3, 5], [4, 4], [5, 5]])
        self.assertEqual(sorted(self.game_state.get_legal_moves(self.game_state.position_player_1)), possible_moves)

    def test_computer_move(self):
        """ Test if the computer makes a move"""

        computer_player1 = ComputerPlayer("HAL2000")
        human_player2 = HumanPlayer("Frank")

        self.game_state = GameBoard(3, 3, computer_player1, human_player2)
        self.game_state.active_player = computer_player1
        self.game_state.positions[self.game_state.player_1] = [0, 1]
        self.game_state.positions[self.game_state.player_2] = [1, 1]
        occupied_positions = [[1, 0], [2, 1], [1, 1], [0, 1]]
        for position in occupied_positions:
            y = position[0]
            x = position[1]
            self.game_state._board[y][x] = True

        move = computer_player1.minimax_decision(self.game_state)
        print(move)
        self.assertEqual(move, [1, 2])

    def test_computer_depth_move(self):
        """ Test if the computer makes a move"""

        computer_player1 = ComputerPlayer("HAL2000")
        human_player2 = HumanPlayer("Frank")

        self.game_state = GameBoard(5, 5, computer_player1, human_player2)
        self.game_state.active_player = computer_player1
        self.game_state.positions[self.game_state.player_1] = [2, 3]
        self.game_state.positions[self.game_state.player_2] = [4, 1]
        occupied_positions = [[1, 0], [2, 1], [1, 1], [0, 1]]
        for position in occupied_positions:
            y = position[0]
            x = position[1]
            self.game_state._board[y][x] = True

        move = computer_player1.minimax_decision(self.game_state, depth=2)
        print(move)
        self.assertEqual(move, [3, 2])

    def test_computer_alpa_beta_pruning(self):
        """ Test if the computer makes a move"""

        computer_player1 = ComputerPlayer("HAL2000")
        human_player2 = HumanPlayer("Frank")

        self.game_state = GameBoard(5, 5, computer_player1, human_player2)
        self.game_state.active_player = computer_player1
        self.game_state.positions[self.game_state.player_1] = [2, 3]
        self.game_state.positions[self.game_state.player_2] = [4, 1]
        occupied_positions = [[1, 0], [2, 1], [1, 1], [0, 1]]
        for position in occupied_positions:
            y = position[0]
            x = position[1]
            self.game_state._board[y][x] = True

        move = computer_player1.alpha_beta_search(self.game_state)
        print(move)
        self.assertEqual(move, [3, 2])


    def test_game_play(self):
        """
        Run the game to check if the game plays out correctly. Should be a short game (<10 moves) where I check if
        the:
        1. Players change initiative every move
        2. The correct available moves are given every turn
        3. The correct board is given every turn
        4. The game ends according to the rules



        Returns:

        """
        pass
