import pygame
import settings

pygame.init()

screen = pygame.display.set_mode(
    (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
)

pygame.display.set_caption(settings.WINDOW_TITLE)

clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.Font(None, 38)
button_font = pygame.font.Font(None, 42)
status_font = pygame.font.Font(None, 28)
restart_font = pygame.font.Font(None, 24)
score_font = pygame.font.Font(None, 24)

ai_thinking = False
ai_thinking_started = 0

selected_player = None
current_player = None

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

round_over = False

x_button = pygame.Rect(190, 75, 90, 50)
o_button = pygame.Rect(320, 75, 90, 50)
restart_button = pygame.Rect(235, 135, 130, 30)

board_rect = pygame.Rect(
    settings.BOARD_X,
    settings.BOARD_Y,
    settings.BOARD_SIZE,
    settings.BOARD_SIZE
)

def draw_neon_text(surface, text, font, color, center):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)

    glow_surface = pygame.Surface(
        text_surface.get_size(),
        pygame.SRCALPHA
    )

    glow_surface.blit(text_surface, (0, 0))

    for offset in [
        (-3, 0), (3, 0),
        (0, -3), (0, 3),
        (-2, -2), (2, 2),
        (-2, 2), (2, -2)
    ]:
        glow_layer = glow_surface.copy()
        glow_layer.set_alpha(45)
        surface.blit(
            glow_layer,
            (text_rect.x + offset[0], text_rect.y + offset[1])
        )

    surface.blit(text_surface, text_rect)


def draw_button(rect, text, color, selected=False):
    pygame.draw.rect(
        screen,
        settings.BUTTON_BACKGROUND,
        rect,
        border_radius=8
    )

    if selected:
        glow_surface = pygame.Surface(
            (rect.width + 24, rect.height + 24),
            pygame.SRCALPHA
        )

        glow_rect = pygame.Rect(
            12, 12,
            rect.width, rect.height
        )

        for width, alpha in [(10, 25), (6, 45), (3, 80)]:
            pygame.draw.rect(
                glow_surface,
                (*color, alpha),
                glow_rect,
                width=width,
                border_radius=8
            )

        screen.blit(
            glow_surface,
            (rect.x - 12, rect.y - 12)
        )

    border_color = color if selected else settings.GRID_COLOR

    pygame.draw.rect(
        screen,
        border_color,
        rect,
        width=2,
        border_radius=8
    )

    draw_neon_text(
        screen,
        text,
        button_font,
        color,
        rect.center
    )


def draw_board():
    for i in range(1, 3):
        x = round(settings.BOARD_X + i * settings.CELL_SIZE)

        pygame.draw.line(
            screen,
            settings.GRID_COLOR,
            (x, settings.BOARD_Y),
            (x, settings.BOARD_Y + settings.BOARD_SIZE),
            2
        )

    for i in range(1, 3):
        y = round(settings.BOARD_Y + i * settings.CELL_SIZE)

        pygame.draw.line(
            screen,
            settings.GRID_COLOR,
            (settings.BOARD_X, y),
            (settings.BOARD_X + settings.BOARD_SIZE, y),
            2
        )


def draw_neon_symbol(symbol, center, color):
    glow_surface = pygame.Surface(
        screen.get_size(),
        pygame.SRCALPHA
    )

    center_x, center_y = center
    margin = 38

    if symbol == "X":
        start_1 = (center_x - margin, center_y - margin)
        end_1 = (center_x + margin, center_y + margin)

        start_2 = (center_x + margin, center_y - margin)
        end_2 = (center_x - margin, center_y + margin)

        draw_shape = lambda target, width, draw_color: (
            pygame.draw.line(target, draw_color, start_1, end_1, width),
            pygame.draw.line(target, draw_color, start_2, end_2, width)
        )

    else:
        radius = 38

        draw_shape = lambda target, width, draw_color: (
            pygame.draw.circle(
                target,
                draw_color,
                center,
                radius,
                width
            )
        )

    # Glow layers
    for width, alpha in [(22, 20), (15, 40), (9, 80)]:
        draw_shape(
            glow_surface,
            width,
            (*color, alpha)
        )

    screen.blit(glow_surface, (0, 0))

    # Bright symbol core
    draw_shape(screen, 5, color)


def draw_symbols():
    for row in range(3):
        for col in range(3):
            symbol = board[row][col]

            if symbol is None:
                continue

            center_x = round(
                settings.BOARD_X + col * settings.CELL_SIZE + settings.CELL_SIZE / 2
            )

            center_y = round(
                settings.BOARD_Y + row * settings.CELL_SIZE + settings.CELL_SIZE / 2
            )

            color = settings.NEON_RED if symbol == "X" else settings.NEON_BLUE

            draw_neon_symbol(
                symbol,
                (center_x, center_y),
                color
            )


def draw_restart_button():
    pygame.draw.rect(
        screen,
        settings.BUTTON_BACKGROUND,
        restart_button,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        settings.GRID_COLOR,
        restart_button,
        width=2,
        border_radius=8
    )

    text = restart_font.render("RESTART", True, settings.WHITE)
    text_rect = text.get_rect(center=restart_button.center)

    screen.blit(text, text_rect)


def draw_scoreboard():
    score_text = (
        f"X: {scores['X']}     "
        f"DRAWS: {scores['draws']}     "
        f"O: {scores['O']}"
    )

    text_surface = score_font.render(
        score_text,
        True,
        settings.WHITE
    )

    text_rect = text_surface.get_rect(
        center=(settings.WINDOW_WIDTH // 2, 180)
    )

    screen.blit(text_surface, text_rect)

def check_winner():
    for row in board:
        if row[0] is not None and row[0] == row[1] == row[2]:
            return row[0]

    for col in range(3):
        if (
            board[0][col] is not None
            and board[0][col] == board[1][col] == board[2][col]
        ):
            return board[0][col]

    if (
        board[0][0] is not None
        and board[0][0] == board[1][1] == board[2][2]
    ):
        return board[0][0]

    if (
        board[0][2] is not None
        and board[0][2] == board[1][1] == board[2][0]
    ):
        return board[0][2]

    return None


def is_draw():
    return all(
        cell is not None
        for row in board
        for cell in row
    )

def reset_board():
    global round_over, current_player, ai_thinking

    for row in board:
        row[:] = [None, None, None]

    current_player = selected_player
    round_over = False
    ai_thinking = False

def switch_player():
    global current_player

    current_player = "O" if current_player == "X" else "X"


def minimax(ai_symbol, human_symbol, is_maximizing, depth=0):

    winner = check_winner()

    if winner == ai_symbol:
        return 10 - depth

    if winner == human_symbol:
        return depth - 10

    if is_draw():
        return 0

    best_score = float("-inf") if is_maximizing else float("inf")

    for row in range(3):
        for col in range(3):

            if board[row][col] is None:

                if is_maximizing:
                    board[row][col] = ai_symbol

                    score = minimax(
                        ai_symbol,
                        human_symbol,
                        False,
                        depth + 1
                    )

                    best_score = max(best_score, score)

                else:
                    board[row][col] = human_symbol

                    score = minimax(
                        ai_symbol,
                        human_symbol,
                        True,
                        depth + 1
                    )

                    best_score = min(best_score, score)

                board[row][col] = None

    return best_score


def make_ai_move():
    global round_over

    ai_symbol = "O" if selected_player == "X" else "X"
    human_symbol = selected_player

    best_score = float("-inf")
    best_move = None

    for row in range(3):
        for col in range(3):

            if board[row][col] is None:

                board[row][col] = ai_symbol

                score = minimax(
                    ai_symbol,
                    human_symbol,
                    False
                )

                board[row][col] = None

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move is None:
        return

    row, col = best_move
    board[row][col] = ai_symbol

    winner = check_winner()

    if winner:
        scores[winner] += 1
        round_over = True

    elif is_draw():
        scores["draws"] += 1
        round_over = True

def draw_game():
    screen.fill(settings.BLACK)

    title = title_font.render("CHOOSE YOUR SIDE", True, settings.WHITE)
    title_rect = title.get_rect(center=(settings.WINDOW_WIDTH // 2, 35))
    screen.blit(title, title_rect)

    draw_button(
        x_button,
        "X",
        settings.NEON_RED,
        selected_player == "X"
    )

    draw_button(
        o_button,
        "O",
        settings.NEON_BLUE,
        selected_player == "O"
    )

    draw_restart_button()
    draw_scoreboard()

    draw_board()
    draw_symbols()

    winner = check_winner()

    if winner:
        status_text = f"{winner} WINS!"

    elif is_draw():
        status_text = "IT'S A DRAW!"

    elif ai_thinking:
        dots = "." * (
                (pygame.time.get_ticks() // 300) % 4
        )

        status_text = f"AI IS THINKING{dots}"

    elif current_player:
        status_text = f"{current_player}'s TURN"

    else:
        status_text = "Select X or O to start"

    status = status_font.render(status_text, True, settings.WHITE)
    status_rect = status.get_rect(
        center=(settings.WINDOW_WIDTH // 2, 580)
    )
    screen.blit(status, status_rect)
    pygame.display.flip()


running = True

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if restart_button.collidepoint(event.pos):
                reset_board()

            elif x_button.collidepoint(event.pos):
                if not any(any(cell is not None for cell in row) for row in board):
                    selected_player = "X"
                    current_player = "X"
                    round_over = False
                    ai_thinking = False

            elif o_button.collidepoint(event.pos):
                if not any(any(cell is not None for cell in row) for row in board):
                    selected_player = "O"
                    current_player = "O"
                    round_over = False
                    ai_thinking = False

            elif (
                selected_player
                and not round_over
                and not ai_thinking
                and board_rect.collidepoint(event.pos)
            ):

                mouse_x, mouse_y = event.pos

                col = int((mouse_x - settings.BOARD_X) // settings.CELL_SIZE)
                row = int((mouse_y - settings.BOARD_Y) // settings.CELL_SIZE)

                if board[row][col] is None:

                    board[row][col] = selected_player

                    winner = check_winner()

                    if winner:
                        scores[winner] += 1
                        round_over = True

                    elif is_draw():
                        scores["draws"] += 1
                        round_over = True

                    else:
                        ai_thinking = True
                        ai_thinking_started = pygame.time.get_ticks()

    if ai_thinking:
        current_time = pygame.time.get_ticks()

        if current_time - ai_thinking_started >= settings.AI_THINKING_DELAY:
            ai_thinking = False
            make_ai_move()

    draw_game()

    clock.tick(60)

pygame.quit()
