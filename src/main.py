import logging

from chess import Board, Move

from src.habits1 import search

logger = logging.getLogger(__name__)


def lambda_handler(event, context) -> Move:
    fen = event['fen']
    board = Board(fen)
    move = search(board)
    return move.uci()
