from chess import Board, Move

from src.habits1 import sort_moves, get_priority_map, get_priority, search


def test_search():
    board = Board("rnbqkbnr/1p4pp/p1ppp3/8/3PKP2/8/PPP3PP/RNBQ1BNR b kq - 0 16")
    move = search(board)


def test_sort_moves():
    board = Board("2kr1bn1/pb1qp3/npP4r/5Pp1/8/5N2/PP3PPP/RNBQKB1R w KQ g6 0 12")
    moves = sort_moves(board)
    print(moves)
    priority_map = get_priority_map(board)
    print(priority_map)


def test_get_priority():
    board = Board("2kr1bn1/pb1qp3/npP4r/5Pp1/8/5N2/PP3PPP/RNBQKB1R w KQ g6 0 12")
    expected_to_moves = {
        0: 'f3g5',  # Capture hanging piece
        0: 'c1g5',  # Capture hanging piece
        0: 'c6b7',  # Capture higher value piece
        1: 'f1a6',  # Equal trade
        1: 'd1d7',  # Equal trade
        1: 'f5g6',  # Equal trade
        2: 'd1d3',  # Save hanging piece
        2: 'f1b5',  # Save hanging piece
        # 4: 'c1e3',  # Center move
        # 5: 'a2a3',  # Not losing material
        6: 'b2b4'
    }
    for expected_priority, move in expected_to_moves.items():
        assert expected_priority == get_priority(board, Move.from_uci(move))
