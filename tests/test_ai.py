import pytest
import ai
import game_logic

AI = "X"
HUMAN = "O"


def create_empty_board():
    return [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]


def test_minimax_returns_positive_score_when_ai_wins():
    board = [
        ["X", "X", "X"],
        ["O", "O", None],
        [None, None, None],
    ]

    score = ai.minimax(board, AI, HUMAN, True)

    assert score == 10


def test_minimax_returns_negative_score_when_human_wins():
    board = [
        ["O", "O", "O"],
        ["X", "X", None],
        [None, None, None],
    ]

    score = ai.minimax(board, AI, HUMAN, True)

    assert score == -10


def test_minimax_returns_zero_for_draw():
    board = [
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", "X"],
    ]

    score = ai.minimax(board, AI, HUMAN, True)

    assert score == 0


def test_ai_takes_winning_move():
    board = [
        ["X", "X", None],
        ["O", "O", None],
        [None, None, None],
    ]

    move = ai.get_best_move(board, AI, HUMAN)

    assert move == (0, 2)


def test_ai_blocks_human_winning_move():
    board = [
        ["O", "O", None],
        ["X", None, None],
        [None, "X", None],
    ]

    move = ai.get_best_move(board, AI, HUMAN)

    assert move == (0, 2)


def test_ai_does_not_modify_original_board():
    board = [
        ["X", None, None],
        ["O", None, None],
        [None, None, None],
    ]

    original_board = [row.copy() for row in board]

    ai.get_best_move(board, AI, HUMAN)

    assert board == original_board


def test_ai_returns_none_when_board_is_full():
    board = [
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", "X"],
    ]

    move = ai.get_best_move(board, AI, HUMAN)

    assert move is None


def test_ai_returns_none_when_board_has_no_empty_cells():
    board = [
        ["X", "X", "X"],
        ["O", "O", "O"],
        ["X", "O", "X"],
    ]

    move = ai.get_best_move(board, AI, HUMAN)

    assert move is None
