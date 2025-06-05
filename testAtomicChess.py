import unittest
from ChessVar import ChessVar  # Replace with your actual module name

class TestAtomicChess(unittest.TestCase):
    def setUp(self):
        self.game = ChessVar()

    def test_opening_sequence(self):
        """Test a typical opening sequence of moves"""
        self.assertTrue(self.game.make_move('d2', 'd4'), "White d2 to d4 should be valid")
        self.assertTrue(self.game.make_move('g7', 'g5'), "Black g7 to g5 should be valid")
        self.assertTrue(self.game.make_move('c1', 'g5'), "White bishop should capture on g5")
        
        self.assertEqual(self.game.get_game_state(), "UNFINISHED", "Game should still be unfinished")

    def test_extended_gameplay_sequence(self):
        """Test a longer sequence of valid moves that doesn't end the game"""
        moves = [
            ('d2', 'd4'), ('g7', 'g5'), ('c1', 'g5'), ('e7', 'e5'),
            ('g2', 'g4'), ('e1', 'e2'), ('e5', 'e4'), ('e2', 'e3'),
            ('e8', 'e7'), ('e3', 'e2'), ('e7', 'e6'), ('f2', 'f3'),
            ('e6', 'e5'), ('e2', 'd3'), ('a7', 'a6'), ('f3', 'e4')
        ]

        for move_from, move_to in moves:
            with self.subTest(move=f"{move_from} -> {move_to}"):
                self.assertTrue(
                    self.game.make_move(move_from, move_to),
                    f"Move {move_from} -> {move_to} should be valid"
                )

        print("\nBoard after extended sequence:")
        self.game.print_board()
        self.assertEqual(self.game.get_game_state(), "UNFINISHED")

    def test_invalid_moves(self):
        """Check that obviously invalid moves are rejected"""
        self.assertFalse(self.game.make_move('e2', 'e5'), "Pawn can't jump 3 squares")
        self.assertFalse(self.game.make_move('a1', 'a1'), "No move made")
        self.assertFalse(self.game.make_move('z9', 'a1'), "Invalid square")
        self.assertFalse(self.game.make_move('d7', 'd6'), "Black can't move first")

    def test_illegal_capture(self):
        """Try to move to a square occupied by own piece"""
        self.game.make_move('d2', 'd4')  # White
        self.assertFalse(
            self.game.make_move('e1', 'd2'),
            "Shouldn't be able to capture own piece"
        )

    def test_game_ends_on_king_explosion(self):
        """Simulate a king being captured to end the game"""
        self.game.make_move('e2', 'e4')  # White
        self.game.make_move('f7', 'f5')  # Black
        self.game.make_move('d1', 'h5')  # White queen out
        self.game.make_move('g7', 'g5')  # Black
        self.game.make_move('h5', 'g5')  # Queen captures near king zone (assumes explosion kills king)

        print("\nBoard after potential king explosion:")
        self.game.print_board()
        self.assertEqual(
            self.game.get_game_state(),
            "WHITE_WON",  # or "FINISHED", depending on your engine
            "Game should end if black king is destroyed"
        )

if __name__ == "__main__":
    unittest.main()