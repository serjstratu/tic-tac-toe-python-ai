import pygame

pygame.init()

# Window settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Tic-Tac-Toe"

#colors
BLACK = (0, 0, 0)
NEON_RED = (255, 23, 68)
NEON_CITRUS = (223, 255, 0)
GRID_COLOR = (35, 35, 45)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()
