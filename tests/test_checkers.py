import unittest

from src.agent import AlphaBetaAgent, evaluate
from src.checkers import BLACK, RED, Board, apply_move, legal_moves


class CheckersRuleTests(unittest.TestCase):
    def test_initial_position_has_seven_black_quiet_moves(self):
        self.assertEqual(len(legal_moves(Board.initial(), BLACK)), 7)

    def test_capture_is_forced_over_a_quiet_move(self):
        board = Board.from_rows((
            "........", "........", ".b......", "..r.....",
            "........", "......b.", "........", "........",
        ))
        moves = legal_moves(board, BLACK)
        self.assertEqual([move.notation() for move in moves], ["9x18"])

    def test_capture_chain_is_one_complete_legal_turn(self):
        board = Board.from_rows((
            "........", "........", ".b......", "..r.....",
            "........", "....r...", "........", "........",
        ))
        move = legal_moves(board, BLACK)[0]
        self.assertEqual(move.notation(), "9x18x27")
        after = apply_move(board, move)
        self.assertEqual(after.at((6, 5)), "b")
        self.assertEqual(after.at((3, 2)), ".")
        self.assertEqual(after.at((5, 4)), ".")

    def test_agent_obeys_forced_capture_at_search_root(self):
        board = Board.from_rows((
            "........", "........", ".b......", "..r.....",
            "........", "......b.", "........", "........",
        ))
        move = AlphaBetaAgent(BLACK, depth=3).choose_move(board)
        self.assertTrue(move.is_capture)
        self.assertEqual(move.notation(), "9x18")

    def test_evaluation_rewards_extra_own_piece(self):
        board = Board.from_rows((
            "........", "........", ".b......", "........",
            "........", "......r.", "........", "........",
        ))
        better = board.with_piece((4, 1), "b")
        self.assertGreater(evaluate(better, BLACK), evaluate(board, BLACK))


if __name__ == "__main__":
    unittest.main()
