from board import Board


def test_constructor():
    # Test minimal required constructor args
    sqaure_size = 100
    square_num = 2
    # passed dummy value for dark_color and light_color since it's a processing syntax
    board = Board(sqaure_size, square_num, 0, 0)
    assert board.size == sqaure_size and \
        board.board == [[0,0],[0,0]] and \
        board.num == square_num 
            
    # Test with optional size value
    sqaure_size_2 = 3
    board_2 = Board(sqaure_size_2, square_num, 0, 0)
    assert board_2.size == sqaure_size_2 and \
        board_2.board == [[0, 0],[0, 0]]

    # Test with insufficient arguments
    try:
        b = Board()
    except TypeError:
        failedWithTypeError = True
    assert failedWithTypeError
