"""Alpha-beta adversarial-search agent for checkers."""
from __future__ import annotations

from math import inf

from .checkers import BLACK, Board, Move, apply_move, belongs_to, is_king, legal_moves, opponent, piece_count

WIN_SCORE = 100_000


def evaluate(board: Board, perspective: str) -> int:
    """Score material, kings, centre occupancy, and side-to-move-independent mobility."""
    other = opponent(perspective)
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board.at((row, col))
            if not belongs_to(piece, perspective) and not belongs_to(piece, other):
                continue
            sign = 1 if belongs_to(piece, perspective) else -1
            value = 100 + (75 if is_king(piece) else 0)
            if 2 <= row <= 5 and 2 <= col <= 5:
                value += 8
            # Men closer to promotion are modestly preferred.
            if not is_king(piece):
                value += (row if piece == BLACK else 7 - row) * 3
            score += sign * value
    score += 3 * (len(legal_moves(board, perspective)) - len(legal_moves(board, other)))
    return score


class AlphaBetaAgent:
    def __init__(self, side: str = BLACK, depth: int = 5) -> None:
        self.side = side
        self.depth = depth
        self.nodes = 0

    def choose_move(self, board: Board) -> Move | None:
        self.nodes = 0
        moves = legal_moves(board, self.side)
        if not moves:
            return None
        best_value = -inf
        best_move = moves[0]
        alpha, beta = -inf, inf
        for move in self._ordered(moves):
            value = self._search(apply_move(board, move), opponent(self.side), self.depth - 1, alpha, beta)
            if value > best_value:
                best_value, best_move = value, move
            alpha = max(alpha, best_value)
        return best_move

    def _search(self, board: Board, turn: str, depth: int, alpha: float, beta: float) -> float:
        self.nodes += 1
        moves = legal_moves(board, turn)
        if not moves:
            return -WIN_SCORE - depth if turn == self.side else WIN_SCORE + depth
        if depth == 0:
            return evaluate(board, self.side)
        maximizing = turn == self.side
        value = -inf if maximizing else inf
        for move in self._ordered(moves):
            child = self._search(apply_move(board, move), opponent(turn), depth - 1, alpha, beta)
            if maximizing:
                value = max(value, child)
                alpha = max(alpha, value)
            else:
                value = min(value, child)
                beta = min(beta, value)
            if alpha >= beta:
                break
        return value

    @staticmethod
    def _ordered(moves: list[Move]) -> list[Move]:
        return sorted(moves, key=lambda move: (move.is_capture, len(move.captures)), reverse=True)
