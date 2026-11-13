# tiny-chess-01 — "Rebahan Engine"

A chess engine in a single Python file (4,081 of the 4,096 bytes allowed),
written for the make.fun tiny-chess-01 competition. Standard library only.

Design, in one breath: 0x88 board representation, full legal move generation
(castling, en passant, promotions — verified against known perft counts),
negamax search with alpha-beta pruning, MVV-LVA move ordering, a
capture-only quiescence search so it never stops counting in the middle of
an exchange, and a pawn piece-square table on top of material values.

The search budget is a fixed node count (40,000), never a clock: the same
position always produces the same move, so a replay of any game matches
the live run move for move.

It plays the gauntlet through the env at `MAKEFUN_ENV_URL`: `POST /game`
for the game in play, `POST /move` with a UCI move, until the env reports
the gauntlet done.
