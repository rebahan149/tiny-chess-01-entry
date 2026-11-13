# tiny-chess-01 — "Rebahan Engine"

A chess engine in a single Python file (4,090 of the 4,096 bytes allowed),
written for the make.fun tiny-chess-01 competition. Standard library only.

Design, in one breath: 0x88 board representation, full legal move generation
(castling, en passant, promotions — verified against known perft counts),
negamax search with alpha-beta pruning, MVV-LVA move ordering, a
capture-only quiescence search so it never stops counting in the middle of
an exchange, and pawn and knight piece-square tables on top of material
values.

The root search is two-phase: every legal move is first scored by
quiescence alone, then only the best few are searched five plies deep,
each with its own fixed slice of the node budget — never a clock: the
same position always produces the same move, so a replay of any game
matches the live run move for move.

It plays the gauntlet through the env at `MAKEFUN_ENV_URL`: `POST /game`
for the game in play, `POST /move` with a UCI move, until the env reports
the gauntlet done.
