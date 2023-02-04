import logging
import random
from typing import List, Dict

from chess import Board, Move

from src.chess_util import is_free_capture, is_saving_hanging_piece, is_equal_trade, is_move_towards_center, \
    is_higher_value_capture, is_losing_material

logger = logging.getLogger(__name__)


def search(board: Board) -> Move:
    try:
        sorted_moves = sort_moves(board)
        return sorted_moves[0]
    except Exception:
        logger.exception("Issue with search")
        raise


def sort_moves(board: Board) -> List[Move]:
    moves_to_priorities = get_priority_map(board)

    def priority_getter(value):
        return moves_to_priorities.get(value)

    return sorted(moves_to_priorities, key=priority_getter)


def get_priority_map(board: Board) -> Dict[Move, int]:
    """
    Maps moves to their priority.
    """
    moves_to_priorities = {}
    moves = list(board.legal_moves)
    random.shuffle(moves)  # Helps to add variety to moves
    for move in moves:
        moves_to_priorities[move] = get_priority(board, move)
    return moves_to_priorities


def get_priority(board: Board, move: Move) -> int:
    # TODO: King towards center and attack pawns
    # TODO: Random pawn moves last
    # TODO: Add checks
    # TODO: Focus more on piece dev - center pawns, then pieces, rooks, queen
    # TODO: Create luft
    if is_free_capture(board, move) or is_higher_value_capture(board, move):
        return 0
    elif is_equal_trade(board, move):
        return 1
    elif is_saving_hanging_piece(board, move):
        return 2
    elif board.is_castling(move):
        return 3
    elif is_move_towards_center(board, move) and not is_losing_material(board, move):
        return 4
    elif not is_losing_material(board, move):
        return 5
    else:
        return 6
