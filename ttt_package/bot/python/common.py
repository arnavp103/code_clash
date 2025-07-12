from typing import Literal

type JSONBoard = list[list[Literal["X", "O", ""]]]
type Move = tuple[int, int]
type Player = Literal["X", "O"]
type BitBoard = list[int]

TIE_EVALUATION: float = 0
