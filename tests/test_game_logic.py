from game_logic import (
    check_winner,
    is_draw,
    reset_board,
    switch_player,
)

# check_winner
def test_check_winner_horizontal():
    board = [
        ["X", "X", "X"],
        ["O", None, "O"],
        [None, None, None],
    ]

    assert check_winner(board) == "X"


def test_check_winner_vertical():
    board = [
        ["O", "X", None],
        ["O", "X", None],
        [None, "X", None],
    ]

    assert check_winner(board) == "X"


def test_check_winner_diagonal():
    board = [
        ["X", "O", None],
        ["O", "X", None],
        [None, None, "X"],
    ]

    assert check_winner(board) == "X"


def test_check_winner_reverse_diagonal():
    board = [
        [None, None, "O"],
        ["X", "O", "X"],
        ["O", None, None],
    ]

    assert check_winner(board) == "O"


def test_check_winner_no_winner():
    board = [
        ["X", "O", "X"],
        ["O", "X", "O"],
        ["O", "X", "O"],
    ]

    assert check_winner(board) is None


def test_check_winner_empty_board():
    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    assert check_winner(board) is None


# is_draw

def test_is_draw_full_board_without_winner():
    board = [
        ["X", "O", "X"],
        ["O", "X", "O"],
        ["O", "X", "O"],
    ]

    assert is_draw(board) is True


def test_is_draw_board_with_empty_cells():
    board = [
        ["X", "O", "X"],
        ["O", None, "O"],
        ["O", "X", "O"],
    ]

    assert is_draw(board) is False


def test_is_draw_empty_board():
    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]

    assert is_draw(board) is False


# reset_board

def test_reset_board():
    board = [
        ["X", "O", "X"],
        ["O", "X", "O"],
        ["X", "O", "X"],
    ]

    reset_board(board)

    assert board == [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]


# switch_player

def test_switch_player_from_x_to_o():
    assert switch_player("X") == "O"


def test_switch_player_from_o_to_x():
    assert switch_player("O") == "X"
