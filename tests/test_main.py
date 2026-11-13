
import pygame
import pytest

from main import Game
import settings
import game_ui


@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def game():
    return Game()


def get_cell_center(row, col):
    return (
        settings.BOARD_X + col * settings.CELL_SIZE
        + settings.CELL_SIZE // 2,

        settings.BOARD_Y + row * settings.CELL_SIZE
        + settings.CELL_SIZE // 2
    )


def click_event(position):
    return pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        {"pos": position, "button": 1}
    )


def test_game_initial_state(game):
    assert game.selected_player is None
    assert game.current_player is None
    assert game.ai_thinking is False
    assert game.running is True
    assert game.is_board_empty()


def test_select_x(game):
    game.select_player("X")

    assert game.selected_player == "X"
    assert game.current_player == "X"
    assert game.ai_thinking is False


def test_select_o_starts_ai(game):
    game.select_player("O")

    assert game.selected_player == "O"
    assert game.ai_thinking is True


def test_cannot_change_player_during_game(game):
    game.select_player("X")
    game.board[0][0] = "X"

    game.select_player("O")

    assert game.selected_player == "X"


def test_human_can_make_move(game):
    game.select_player("X")

    game.handle_human_move(get_cell_center(0, 0))

    assert game.board[0][0] == "X"
    assert game.ai_thinking is True


def test_human_cannot_make_move_outside_board(game):
    game.select_player("X")

    game.handle_human_move((10, 10))

    assert game.is_board_empty()


def test_human_cannot_overwrite_cell(game):
    game.select_player("X")
    game.board[0][0] = "X"

    game.handle_human_move(get_cell_center(0, 0))

    assert game.board[0][0] == "X"


def test_human_cannot_move_while_ai_is_thinking(game):
    game.select_player("X")
    game.ai_thinking = True

    game.handle_human_move(get_cell_center(0, 0))

    assert game.is_board_empty()


def test_ai_move(game, monkeypatch):
    game.select_player("X")

    monkeypatch.setattr(
        "main.ai.get_best_move",
        lambda *args: (1, 1)
    )

    game.handle_ai_move()

    assert game.board[1][1] == "O"


def test_ai_move_updates_score(game, monkeypatch):
    game.select_player("X")

    game.board[0] = ["O", "O", None]

    monkeypatch.setattr(
        "main.ai.get_best_move",
        lambda *args: (0, 2)
    )

    game.handle_ai_move()

    assert game.scores["O"] == 1


def test_ai_move_resets_thinking_state_after_delay(game, monkeypatch):
    game.select_player("X")

    monkeypatch.setattr(
        "main.ai.get_best_move",
        lambda *args: (1, 1)
    )

    game.ai_thinking = True
    game.ai_thinking_started = 1000

    game.update(1000 + settings.AI_THINKING_DELAY)

    assert game.ai_thinking is False
    assert game.board[1][1] == "O"


def test_ai_does_not_move_before_delay(game, monkeypatch):
    game.select_player("X")

    monkeypatch.setattr(
        "main.ai.get_best_move",
        lambda *args: (1, 1)
    )

    game.ai_thinking = True
    game.ai_thinking_started = 1000

    game.update(1000)

    assert game.ai_thinking is True
    assert game.is_board_empty()


def test_human_win_updates_score(game):
    game.select_player("X")

    game.board[0] = ["X", "X", None]

    game.handle_human_move(get_cell_center(0, 2))

    assert game.scores["X"] == 1
    assert game.ai_thinking is False


def test_restart_resets_board(game):
    game.select_player("X")
    game.board[0][0] = "X"
    game.board[1][1] = "O"

    game.restart()

    assert game.is_board_empty()
    assert game.current_player == "X"
    assert game.ai_thinking is False


def test_restart_preserves_scores(game):
    game.scores = {
        "X": 3,
        "O": 2,
        "draws": 1
    }

    game.select_player("X")
    game.restart()

    assert game.scores == {
        "X": 3,
        "O": 2,
        "draws": 1
    }


def test_restart_starts_ai_when_human_selected_o(game):
    game.select_player("O")
    game.ai_thinking = False

    game.restart()

    assert game.ai_thinking is True


def test_quit_event_stops_game(game):
    event = pygame.event.Event(pygame.QUIT)

    game.handle_event(event)

    assert game.running is False


def test_x_button_selects_x(game):
    game.handle_event(
        click_event(game_ui.X_BUTTON.center)
    )

    assert game.selected_player == "X"


def test_o_button_selects_o(game):
    game.handle_event(
        click_event(game_ui.O_BUTTON.center)
    )

    assert game.selected_player == "O"
    assert game.ai_thinking is True


def test_restart_button_resets_game(game):
    game.select_player("X")
    game.board[0][0] = "X"

    game.handle_event(
        click_event(game_ui.RESTART_BUTTON.center)
    )

    assert game.is_board_empty()
