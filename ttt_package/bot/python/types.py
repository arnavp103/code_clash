from typing import Literal

type Board = list[list[Literal["X", "O", ""]]]
type Evaluation = float
type Move = tuple[int, int]
type EvaluatedMove = tuple[Evaluation, Move]
