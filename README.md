# Checkers Mini AI - Adversarial Search

A small, dependency-free Python implementation of English draughts (checkers)
with an alpha-beta search agent. The key rule is implemented in one place:
when a capture exists, `legal_moves` returns only capturing moves. Multi-jump
capture chains are generated as one complete turn, so search cannot stop after
only the first jump.

## Run

Requires Python 3.10+.

```powershell
python -m unittest discover -s tests -v
python -m src.game --depth 5
```

The game prints a board after each AI move. Black is the AI and red moves are
selected automatically at random for a short demonstration. Use `--human-red`
to enter red moves such as `52-43` (quiet move) or `52x34x16` (capture chain).

## Project layout

- `src/` - board, legal-move generator, evaluation, alpha-beta agent, CLI
- `tests/` - regression tests for movement, mandatory captures, multi-jumps, and search
- `docs/report.pdf` - 2-page project report
- `docs/report_source.py` - reproducible report generator

## Rules implemented

- 8 by 8 board; only dark squares are playable.
- Men move diagonally forward; kings move diagonally in either direction.
- Captures jump an adjacent opponent into the empty square beyond it.
- If one or more captures are available, a non-capture is illegal.
- A player must continue jumping with the same piece while another capture is available.
- A man promotes on reaching the far row; promotion ends that turn (English draughts convention).

## AI approach

The agent uses depth-limited minimax with alpha-beta pruning. It searches the
same `legal_moves` function used by the UI, which ensures mandatory captures
are enforced at every adversarial-search node. Terminal values reward wins and
losses; non-terminal positions use material, king count, mobility, and centre
control. See `docs/report.pdf` for the design and complexity discussion.

## Personalisation

Before submission, replace the student-name/register-number placeholders in
the report source and the README with your own details if your instructor
requires them. The code is intentionally original and uses no third-party
packages.
