import chess
from chess import Board, Move, SquareSet, WHITE

from src.chess_util import is_piece_hanging, is_saving_hanging_piece, is_higher_value_capture, is_losing_material, \
    get_pieces


def test_is_higher_value_capture():
    board = Board("2kr1bn1/pb1qp3/npP4r/5Pp1/8/5N2/PP3PPP/RNBQKB1R w KQ g6 0 12")
    assert is_higher_value_capture(board, Move.from_uci('c6b7'))
    assert not is_higher_value_capture(board, Move.from_uci('f3g5'))


def test_is_piece_hanging():
    board = Board("2kr1bn1/pb1qp3/npP4r/5Pp1/8/5N2/PP3PPP/RNBQKB1R w KQ g6 0 12")
    assert is_piece_hanging(board, chess.G5)
    assert not is_piece_hanging(board, chess.H2)


def test_is_saving_hanging_piece():
    board = Board("2kr1bn1/pb1qp3/npP4r/5Pp1/8/5NP1/PP3P1P/RNBQKB1R b KQ - 0 12")
    assert not is_saving_hanging_piece(board, Move.from_uci('g5g4'))
    assert is_saving_hanging_piece(board, Move.from_uci('h6h5'))
    board = Board("r1b2k1r/ppppn1p1/3b3p/3q1n2/4Q3/1PP1PN2/P5PP/RNB2RK1 w - - 0 15")
    assert not is_saving_hanging_piece(board, Move.from_uci('e4f4'))


def test_get_pieces():
    board = Board("2kr1bn1/pb1qp3/npP4r/5Pp1/8/5N2/PP3PPP/RNBQKB1R w KQ g6 0 12")
    expected_pieces = SquareSet([chess.A1, chess.B1, chess.C1, chess.D1, chess.F1, chess.H1, chess.A2, chess.B2,
                                 chess.C6, chess.F2, chess.F3, chess.F5, chess.G2, chess.H2])
    pieces = get_pieces(board, WHITE)
    assert expected_pieces == pieces


def test_is_losing_material():
    board = Board("r1b2k1r/pppp2p1/2nb1q1p/5n2/2BP4/1PPQPN2/P5PP/RNB2RK1 w - - 0 12")
    assert is_losing_material(board, Move.from_uci('c4f7'))
    board = Board("r1b2k1r/ppppn1p1/3b3p/3q1n2/4Q3/1PP1PN2/P5PP/RNB2RK1 w - - 0 15")
    assert is_losing_material(board, Move.from_uci('e4f4'))
    board = Board("4r1k1/1p3ppp/2n5/p1P1p3/P3P3/2P2PP1/7P/1KNr1B1R w - - 0 37")
    assert is_losing_material(board, Move.from_uci('f1d3'))
