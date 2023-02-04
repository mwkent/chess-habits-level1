import chess
from chess import Board, Move, Square, Color, SquareSet, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING


PIECE_TYPES_TO_VALUES = {PAWN: 1, KNIGHT: 3, BISHOP: 3, ROOK: 5, QUEEN: 9, KING: 10_000}


def is_free_capture(board: Board, move: Move) -> bool:
    # TODO: Should only consider pieces, not pawns?
    # Is capture and no defenders
    return board.is_capture(move) and not board.is_attacked_by(not board.turn, move.to_square)


def value_at(board: Board, piece: Square):
    return PIECE_TYPES_TO_VALUES[board.piece_type_at(piece)]


def is_higher_value_capture(board: Board, move: Move) -> bool:
    return board.is_capture(move) and not board.is_en_passant(move) and \
           value_at(board, move.from_square) < value_at(board, move.to_square)


def get_pieces(board: Board, color: Color) -> SquareSet:
    pieces: SquareSet = SquareSet()
    for piece_type in range(1, 6):  # All piece types except king
        pieces = pieces.union(board.pieces(piece_type, color))
    return pieces


def is_saving_hanging_piece(board: Board, move: Move) -> bool:
    piece_color = board.color_at(move.from_square)
    if is_losing_material(board, move):
        return False
    for piece in get_pieces(board, piece_color):
        if is_piece_hanging(board, piece):
            board.push(move)
            try:
                if (piece == move.from_square and not is_piece_hanging(board, move.to_square)) or \
                        (piece != move.from_square and not is_piece_hanging(board, piece)):
                    return True
            finally:
                board.pop()
    return False


def is_piece_hanging(board: Board, piece: Square) -> bool:
    piece_color = board.color_at(piece)
    return board.is_attacked_by(not piece_color, piece) and not board.is_attacked_by(piece_color, piece)


def is_piece_attacked_by_weaker_piece(board: Board, piece: Square) -> bool:
    piece_color = board.color_at(piece)
    attackers = board.attackers(not piece_color, piece)
    return any(value_at(board, attacker) < value_at(board, piece) for attacker in attackers)


def is_losing_material(board: Board, move: Move) -> bool:
    """
    Does the move hang a piece or sacrifice material (e.g. moves bishop under attack of pawn)
    """
    color = board.color_at(move.from_square)
    pieces_before_move = get_pieces(board, color)
    num_pieces_losing_before_move = 0
    for piece in pieces_before_move:
        if is_piece_hanging(board, piece) or is_piece_attacked_by_weaker_piece(board, piece):
            num_pieces_losing_before_move += 1

    board.push(move)
    try:
        pieces_after_move = get_pieces(board, color)
        num_pieces_losing_after_move = 0
        for piece in pieces_after_move:
            if is_piece_hanging(board, piece) or is_piece_attacked_by_weaker_piece(board, piece):
                num_pieces_losing_after_move += 1
    finally:
        board.pop()

    if num_pieces_losing_after_move > 0 and num_pieces_losing_after_move >= num_pieces_losing_before_move:
        return True
    return False


def is_equal_trade(board: Board, move: Move) -> bool:
    piece_types_to_values = {PAWN: 1, KNIGHT: 3, BISHOP: 3, ROOK: 5, QUEEN: 9}
    return board.is_en_passant(move) or (board.is_capture(move) and
                                         (piece_types_to_values[board.piece_type_at(move.from_square)] ==
                                          piece_types_to_values[board.piece_type_at(move.to_square)]))


def is_move_towards_center(board: Board, move: Move) -> bool:
    center = {chess.C3, chess.C4, chess.C5, chess.C6,
              chess.D3, chess.D4, chess.D5, chess.D6,
              chess.E3, chess.E4, chess.E5, chess.E6,
              chess.F3, chess.F4, chess.F5, chess.F6}
    return move.from_square not in center and move.to_square in center \
           and board.piece_type_at(move.from_square) != chess.KING
