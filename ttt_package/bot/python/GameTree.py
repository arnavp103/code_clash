from typing import Union

from types import Evaluation, Move

type NodeEvaluation = Evaluation | None


class GameTree:
    def __init__(self, evalv: NodeEvaluation, parent: Union['GameTree', None], move_from_parent: Move | None):
        # root should be the only one containing a non-None board
        self.evalv = evalv
        self.parent = parent
        self.move_from_parent: Move | None = move_from_parent
        self.children: dict[Move, GameTree] = {}
        self.pruned = False

    def add_child(self, move: Move, evalv: NodeEvaluation):
        # when move is in children.keys(), the evaluation should be the same so it will not change
        self.children[move] = GameTree(evalv, self, move)

    def remove_child(self, move: Move):
        del self.children[move]
