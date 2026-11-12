
import pygame

pygame.init()

# Window settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Tic-Tac-Toe"

# Colors
BLACK = (0, 0, 0)
NEON_RED = (255, 23, 68)
NEON_CITRUS = (223, 255, 0)
GRID_COLOR = (35, 35, 45)
WHITE = (255, 255, 255)
BUTTON_BACKGROUND = (15, 15, 20)

# Board settings
BOARD_SIZE = 400
BOARD_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
BOARD_Y = 170
CELL_SIZE = BOARD_SIZE / 3

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Fonts
title_font = pygame.font.Font(None, 38)
button_font = pygame.font.Font(None, 42)
status_font = pygame.font.Font(None, 28)

selected_player = None

x_button = pygame.Rect(190, 75, 90, 50)
o_button = pygame.Rect(320, 75, 90, 50)



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
        BUTTON_BACKGROUND,
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

    border_color = color if selected else GRID_COLOR

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
        x = round(BOARD_X + i * CELL_SIZE)

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (x, BOARD_Y),
            (x, BOARD_Y + BOARD_SIZE),
            2
        )

    for i in range(1, 3):
        y = round(BOARD_Y + i * CELL_SIZE)

        pygame.draw.line(
            screen,
            GRID_COLOR,
            (BOARD_X, y),
            (BOARD_X + BOARD_SIZE, y),
            2
        )


def draw_game():
    screen.fill(BLACK)

    title = title_font.render("CHOOSE YOUR SIDE", True, WHITE)
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 35))
    screen.blit(title, title_rect)

    draw_button(
        x_button,
        "X",
        NEON_RED,
        selected_player == "X"
    )

    draw_button(
        o_button,
        "O",
        NEON_CITRUS,
        selected_player == "O"
    )

    draw_board()

    if selected_player:
        status_text = f"You are playing as {selected_player}"
    else:
        status_text = "Select X or O to start"

    status = status_font.render(status_text, True, WHITE)
    status_rect = status.get_rect(
        center=(WINDOW_WIDTH // 2, 590)
    )
    screen.blit(status, status_rect)
    pygame.display.flip()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if x_button.collidepoint(event.pos):
                selected_player = "X"

            elif o_button.collidepoint(event.pos):
                selected_player = "O"

    draw_game()

pygame.quit()
