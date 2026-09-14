"""Small command-line demonstration for the checkers agent."""
from __future__ import annotations

import argparse
import random

from .agent import AlphaBetaAgent
from .checkers import BLACK, RED, Board, apply_move, legal_moves


def main() -> None:
    parser = argparse.ArgumentParser(description="Checkers AI demonstration")
    parser.add_argument("--depth", type=int, default=5, help="alpha-beta ply depth")
    parser.add_argument("--turns", type=int, default=20, help="maximum full turns")
    parser.add_argument("--human-red", action="store_true", help="select red moves by notation")
    args = parser.parse_args()
    board, side = Board.initial(), BLACK
    agent = AlphaBetaAgent(BLACK, args.depth)
    print(board.render())
    for _ in range(args.turns * 2):
        moves = legal_moves(board, side)
        if not moves:
            print(f"{side} has no legal moves. {('red' if side == BLACK else 'black')} wins.")
            return
        if side == BLACK:
            move = agent.choose_move(board)
            print(f"Black AI: {move.notation()} ({agent.nodes} nodes)")
        elif args.human_red:
            print("Red legal moves:", ", ".join(m.notation() for m in moves))
            selected = input("Choose move: ").strip()
            move = next((m for m in moves if m.notation() == selected), None)
            if move is None:
                print("That move is not legal; mandatory captures may apply.")
                continue
        else:
            move = random.choice(moves)
            print(f"Red sample player: {move.notation()}")
        board = apply_move(board, move)
        print(board.render())
        side = RED if side == BLACK else BLACK


if __name__ == "__main__":
    main()
