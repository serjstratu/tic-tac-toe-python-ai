import pygame
import pytest

import game_ui
import settings


@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def screen():
    return pygame.Surface(
        (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
    )


@pytest.fixture
def fonts():
    return {
        "title": pygame.font.Font(None, 38),
        "button": pygame.font.Font(None, 42),
        "restart": pygame.font.Font(None, 28),
        "score": pygame.font.Font(None, 28),
        "status": pygame.font.Font(None, 28),
    }


@pytest.fixture
def empty_board():
    return [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]


@pytest.fixture
def scores():
    return {
        "X": 2,
        "O": 1,
        "draws": 3,
    }


def test_draw_neon_text(screen, fonts):
    game_ui.draw_neon_text(
        screen,
        "TEST",
        fonts["title"],
        settings.WHITE,
        (300, 100)
    )


def test_draw_button(screen, fonts):
    game_ui.draw_button(
        screen,
        game_ui.X_BUTTON,
        "X",
        settings.NEON_RED,
        fonts["button"]
    )


def test_draw_selected_button(screen, fonts):
    game_ui.draw_button(
        screen,
        game_ui.O_BUTTON,
        "O",
        settings.NEON_BLUE,
        fonts["button"],
        selected=True
    )


def test_draw_board(screen):
    game_ui.draw_board(screen)


@pytest.mark.parametrize("symbol", ["X", "O"])
def test_draw_neon_symbol(screen, symbol):
    game_ui.draw_neon_symbol(
        screen,
        symbol,
        (300, 300),
        settings.NEON_RED
    )


def test_draw_symbols(screen, empty_board):
    game_ui.draw_symbols(screen, empty_board)


def test_draw_symbols_with_moves(screen, empty_board):
    empty_board[0][0] = "X"
    empty_board[1][1] = "O"
    empty_board[2][2] = "X"

    game_ui.draw_symbols(screen, empty_board)


def test_draw_restart_button(screen, fonts):
    game_ui.draw_restart_button(screen, fonts["restart"])


def test_draw_scoreboard(screen, scores, fonts):
    game_ui.draw_scoreboard(
        screen,
        scores,
        fonts["score"]
    )


def test_draw_game(screen, fonts, empty_board, scores, monkeypatch):
    monkeypatch.setattr(pygame.display, "flip", lambda: None)

    game_ui.draw_game(
        screen,
        fonts,
        empty_board,
        scores,
        None,
        None,
        False
    )


def test_draw_game_with_ai_thinking(
    screen,
    fonts,
    empty_board,
    scores,
    monkeypatch
):
    monkeypatch.setattr(pygame.display, "flip", lambda: None)

    game_ui.draw_game(
        screen,
        fonts,
        empty_board,
        scores,
        "X",
        None,
        True
    )


def test_draw_game_with_current_player(
    screen,
    fonts,
    empty_board,
    scores,
    monkeypatch
):
    monkeypatch.setattr(pygame.display, "flip", lambda: None)

    game_ui.draw_game(
        screen,
        fonts,
        empty_board,
        scores,
        "X",
        "X",
        False
    )


def test_draw_game_with_winner(
    screen,
    fonts,
    empty_board,
    scores,
    monkeypatch
):
    empty_board[0] = ["X", "X", "X"]

    monkeypatch.setattr(pygame.display, "flip", lambda: None)

    game_ui.draw_game(
        screen,
        fonts,
        empty_board,
        scores,
        "X",
        None,
        False
    )


def test_draw_game_with_draw(
    screen,
    fonts,
    scores,
    monkeypatch
):
    board = [
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", "X"],
    ]

    monkeypatch.setattr(pygame.display, "flip", lambda: None)

    game_ui.draw_game(
        screen,
        fonts,
        board,
        scores,
        "X",
        None,
        False
    )
