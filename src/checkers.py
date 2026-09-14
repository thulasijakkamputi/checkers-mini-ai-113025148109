"""Core rules for an 8x8 English draughts board."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

EMPTY = "."
BLACK, RED = "b", "r"
Coord = tuple[int, int]


def opponent(side: str) -> str:
    return RED if side == BLACK else BLACK


def belongs_to(piece: str, side: str) -> bool:
    return piece.lower() == side


def is_king(piece: str) -> bool:
    return piece.isupper()


def in_bounds(square: Coord) -> bool:
    row, col = square
    return 0 <= row < 8 and 0 <= col < 8


def square_number(square: Coord) -> int:
    """Convert a playable coordinate to conventional checkers numbering 1..32."""
    row, col = square
    if (row + col) % 2 == 0:
        raise ValueError("light squares do not have checkers numbers")
    return row * 4 + (col // 2 + 1)


@dataclass(frozen=True)
class Move:
    path: tuple[Coord, ...]
    captures: tuple[Coord, ...] = ()

    @property
    def is_capture(self) -> bool:
        return bool(self.captures)

    def notation(self) -> str:
        separator = "x" if self.is_capture else "-"
        return separator.join(str(square_number(s)) for s in self.path)


@dataclass(frozen=True)
class Board:
    cells: tuple[str, ...]

    @classmethod
    def initial(cls) -> "Board":
        cells = [EMPTY] * 64
        for row in range(3):
            for col in range(8):
                if (row + col) % 2:
                    cells[row * 8 + col] = BLACK
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2:
                    cells[row * 8 + col] = RED
        return cls(tuple(cells))

    @classmethod
    def from_rows(cls, rows: Iterable[str]) -> "Board":
        rows = tuple(rows)
        if len(rows) != 8 or any(len(row) != 8 for row in rows):
            raise ValueError("board needs exactly eight rows of eight characters")
        return cls(tuple("".join(rows)))

    def at(self, square: Coord) -> str:
        row, col = square
        return self.cells[row * 8 + col]

    def with_piece(self, square: Coord, piece: str) -> "Board":
        row, col = square
        cells = list(self.cells)
        cells[row * 8 + col] = piece
        return Board(tuple(cells))

    def render(self) -> str:
        lines = ["    0 1 2 3 4 5 6 7"]
        for row in range(8):
            lines.append(f"{row} | " + " ".join(self.at((row, col)) for col in range(8)))
        return "\n".join(lines)


def directions(piece: str) -> tuple[tuple[int, int], ...]:
    if is_king(piece):
        return ((-1, -1), (-1, 1), (1, -1), (1, 1))
    step = 1 if piece == BLACK else -1
    return ((step, -1), (step, 1))


def _capture_sequences(board: Board, start: Coord) -> list[Move]:
    """Return complete capture chains from one piece, not individual jumps."""
    piece = board.at(start)
    side = piece.lower()
    found: list[Move] = []

    def visit(position: Coord, state: Board, path: tuple[Coord, ...], taken: tuple[Coord, ...]) -> None:
        moving_piece = state.at(position)
        next_jumps: list[tuple[Coord, Coord]] = []
        for dr, dc in directions(moving_piece):
            jumped = (position[0] + dr, position[1] + dc)
            landing = (position[0] + 2 * dr, position[1] + 2 * dc)
            if in_bounds(landing) and belongs_to(state.at(jumped), opponent(side)) and state.at(landing) == EMPTY:
                next_jumps.append((jumped, landing))
        if not next_jumps:
            if taken:
                found.append(Move(path, taken))
            return
        for jumped, landing in next_jumps:
            next_state = state.with_piece(position, EMPTY).with_piece(jumped, EMPTY)
            landed_piece = moving_piece
            # Reaching king row ends this move under English draughts rules.
            crowned = (moving_piece == BLACK and landing[0] == 7) or (moving_piece == RED and landing[0] == 0)
            if crowned:
                next_state = next_state.with_piece(landing, moving_piece.upper())
                found.append(Move(path + (landing,), taken + (jumped,)))
            else:
                next_state = next_state.with_piece(landing, landed_piece)
                visit(landing, next_state, path + (landing,), taken + (jumped,))

    visit(start, board, (start,), ())
    return found


def legal_moves(board: Board, side: str) -> list[Move]:
    """Generate legal moves, applying the mandatory-capture rule globally."""
    captures: list[Move] = []
    quiet: list[Move] = []
    for row in range(8):
        for col in range(8):
            start = (row, col)
            piece = board.at(start)
            if not belongs_to(piece, side):
                continue
            captures.extend(_capture_sequences(board, start))
            for dr, dc in directions(piece):
                end = (row + dr, col + dc)
                if in_bounds(end) and board.at(end) == EMPTY:
                    quiet.append(Move((start, end)))
    return captures if captures else quiet


def apply_move(board: Board, move: Move) -> Board:
    piece = board.at(move.path[0])
    if piece == EMPTY:
        raise ValueError("move starts on an empty square")
    state = board.with_piece(move.path[0], EMPTY)
    for captured in move.captures:
        state = state.with_piece(captured, EMPTY)
    end = move.path[-1]
    if piece == BLACK and end[0] == 7:
        piece = "B"
    elif piece == RED and end[0] == 0:
        piece = "R"
    return state.with_piece(end, piece)


def piece_count(board: Board, side: str) -> int:
    return sum(belongs_to(piece, side) for piece in board.cells)
