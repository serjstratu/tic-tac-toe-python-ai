import pygame
import settings
import game_ui
import game_logic
import ai


pygame.init()

screen = pygame.display.set_mode(
    (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
)

pygame.display.set_caption(settings.WINDOW_TITLE)

clock = pygame.time.Clock()

# Fonts
fonts = {
    "title": pygame.font.Font(None, 38),
    "button": pygame.font.Font(None, 42),
    "status": pygame.font.Font(None, 28),
    "restart": pygame.font.Font(None, 24),
    "score": pygame.font.Font(None, 24)
}

board = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]

scores = {
    "X": 0,
    "O": 0,
    "draws": 0
}

selected_player = None
current_player = None

ai_thinking = False
ai_thinking_started = 0

running = True


def handle_ai_move():
    global ai_thinking

    ai_symbol = "O" if selected_player == "X" else "X"
    human_symbol = selected_player

    move = ai.get_best_move(
        board,
        ai_symbol,
        human_symbol
    )

    if move is None:
        return

    row, col = move
    board[row][col] = ai_symbol

    winner = game_logic.check_winner(board)

    if winner:
        scores[winner] += 1

    elif game_logic.is_draw(board):
        scores["draws"] += 1


while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_ui.RESTART_BUTTON.collidepoint(event.pos):

                game_logic.reset_board(board)

                current_player = selected_player
                ai_thinking = False

            elif game_ui.X_BUTTON.collidepoint(event.pos):

                if all(
                    cell is None
                    for row in board
                    for cell in row
                ):
                    selected_player = "X"
                    current_player = "X"
                    ai_thinking = False

            elif game_ui.O_BUTTON.collidepoint(event.pos):

                if all(
                    cell is None
                    for row in board
                    for cell in row
                ):
                    selected_player = "O"
                    current_player = "O"
                    ai_thinking = False

            elif (
                selected_player
                and not ai_thinking
                and not game_logic.check_winner(board)
                and not game_logic.is_draw(board)
                and game_ui.BOARD_RECT.collidepoint(event.pos)
            ):

                mouse_x, mouse_y = event.pos

                col = int(
                    (mouse_x - settings.BOARD_X)
                    // settings.CELL_SIZE
                )

                row = int(
                    (mouse_y - settings.BOARD_Y)
                    // settings.CELL_SIZE
                )

                if board[row][col] is None:

                    board[row][col] = selected_player

                    winner = game_logic.check_winner(board)

                    if winner:
                        scores[winner] += 1

                    elif game_logic.is_draw(board):
                        scores["draws"] += 1

                    else:
                        ai_thinking = True
                        ai_thinking_started = pygame.time.get_ticks()

    if ai_thinking:

        current_time = pygame.time.get_ticks()

        if (
            current_time - ai_thinking_started
            >= settings.AI_THINKING_DELAY
        ):
            handle_ai_move()
            ai_thinking = False

    game_ui.draw_game(
        screen,
        fonts,
        board,
        scores,
        selected_player,
        current_player,
        ai_thinking
    )

    clock.tick(60)

pygame.quit()
