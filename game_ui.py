import pygame
import settings
import game_logic


X_BUTTON = pygame.Rect(190, 75, 90, 50)
O_BUTTON = pygame.Rect(320, 75, 90, 50)
RESTART_BUTTON = pygame.Rect(235, 135, 130, 30)

BOARD_RECT = pygame.Rect(
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

    offsets = [
        (-3, 0), (3, 0),
        (0, -3), (0, 3),
        (-2, -2), (2, 2),
        (-2, 2), (2, -2)
    ]

    for offset in offsets:
        glow_layer = glow_surface.copy()
        glow_layer.set_alpha(45)

        surface.blit(
            glow_layer,
            (text_rect.x + offset[0], text_rect.y + offset[1])
        )

    surface.blit(text_surface, text_rect)


def draw_button(screen, rect, text, color, font, selected=False):

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
        font,
        color,
        rect.center
    )


def draw_board(screen):

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


def draw_neon_symbol(screen, symbol, center, color):

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

        def draw_shape(target, width, draw_color):
            pygame.draw.line(
                target, draw_color, start_1, end_1, width
            )
            pygame.draw.line(
                target, draw_color, start_2, end_2, width
            )

    else:
        radius = 38

        def draw_shape(target, width, draw_color):
            pygame.draw.circle(
                target,
                draw_color,
                center,
                radius,
                width
            )

    # Glow layers
    for width, alpha in [(22, 20), (15, 40), (9, 80)]:
        draw_shape(
            glow_surface,
            width,
            (*color, alpha)
        )

    screen.blit(glow_surface, (0, 0))
    draw_shape(screen, 5, color)


def draw_symbols(screen, board):

    for row in range(3):
        for col in range(3):

            symbol = board[row][col]

            if symbol is None:
                continue

            center_x = round(
                settings.BOARD_X
                + col * settings.CELL_SIZE
                + settings.CELL_SIZE / 2
            )

            center_y = round(
                settings.BOARD_Y
                + row * settings.CELL_SIZE
                + settings.CELL_SIZE / 2
            )

            color = (
                settings.NEON_RED
                if symbol == "X"
                else settings.NEON_BLUE
            )

            draw_neon_symbol(
                screen,
                symbol,
                (center_x, center_y),
                color
            )


def draw_restart_button(screen, font):

    pygame.draw.rect(
        screen,
        settings.BUTTON_BACKGROUND,
        RESTART_BUTTON,
        border_radius=8
    )

    pygame.draw.rect(
        screen,
        settings.GRID_COLOR,
        RESTART_BUTTON,
        width=2,
        border_radius=8
    )

    text = font.render("RESTART", True, settings.WHITE)
    text_rect = text.get_rect(center=RESTART_BUTTON.center)

    screen.blit(text, text_rect)


def draw_scoreboard(screen, scores, font):

    score_text = (
        f"X: {scores['X']}     "
        f"DRAWS: {scores['draws']}     "
        f"O: {scores['O']}"
    )

    text_surface = font.render(
        score_text,
        True,
        settings.WHITE
    )

    text_rect = text_surface.get_rect(
        center=(settings.WINDOW_WIDTH // 2, 180)
    )

    screen.blit(text_surface, text_rect)


def draw_game(
    screen,
    fonts,
    board,
    scores,
    selected_player,
    current_player,
    ai_thinking
):

    screen.fill(settings.BLACK)

    title = fonts["title"].render(
        "CHOOSE YOUR SIDE",
        True,
        settings.WHITE
    )

    title_rect = title.get_rect(
        center=(settings.WINDOW_WIDTH // 2, 35)
    )

    screen.blit(title, title_rect)

    draw_button(
        screen,
        X_BUTTON,
        "X",
        settings.NEON_RED,
        fonts["button"],
        selected_player == "X"
    )

    draw_button(
        screen,
        O_BUTTON,
        "O",
        settings.NEON_BLUE,
        fonts["button"],
        selected_player == "O"
    )

    draw_restart_button(screen, fonts["restart"])

    draw_scoreboard(
        screen,
        scores,
        fonts["score"]
    )

    draw_board(screen)
    draw_symbols(screen, board)

    winner = game_logic.check_winner(board)

    if winner:
        status_text = f"{winner} WINS!"

    elif game_logic.is_draw(board):
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

    status = fonts["status"].render(
        status_text,
        True,
        settings.WHITE
    )

    status_rect = status.get_rect(
        center=(settings.WINDOW_WIDTH // 2, 580)
    )

    screen.blit(status, status_rect)

    pygame.display.flip()
