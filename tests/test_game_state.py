import unittest
from Exercises.Isolation.new_game import GameState


class TestGameState(unittest.TestCase):
    def test_game_state(self):
        self.player1 = "player1"
        self.player2 = "player2"
        self.game_state = GameState(6, 8, self.player1, self.player2)

    def test_init(self):
        # Ensure that the game state is initialized correctly
        self.assertEqual(len(self.game_state._board), 6)
        self.assertEqual(len(self.game_state._board[0]), 8)
        self.assertIsNone(self.game_state.position_player_1)
        self.assertIsNone(self.game_state.position_player_2)
        self.assertFalse(self.game_state.game_over)
        self.assertTrue(self.game_state.has_initiative() in [self.player_1, self.player_2])

    def test_get_all_moves(self):
        # Test the get_all_moves method
        all_moves = self.game_state.get_all_moves()
        self.assertEqual(len(all_moves), 6 * 8)

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


