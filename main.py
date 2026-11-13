import pygame
import settings
import game_ui
import game_logic
import ai


class Game:
    def __init__(self):
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

        self.scores = {
            "X": 0,
            "O": 0,
            "draws": 0
        }

        self.selected_player = None
        self.current_player = None

        self.ai_thinking = False
        self.ai_thinking_started = 0
        self.running = True

    def is_board_empty(self):
        return all(
            cell is None
            for row in self.board
            for cell in row
        )

    def is_game_over(self):
        return (
            game_logic.check_winner(self.board) is not None
            or game_logic.is_draw(self.board)
        )

    def select_player(self, symbol):
        if not self.is_board_empty():
            return

        self.selected_player = symbol
        self.current_player = symbol
        self.ai_thinking = False

        if symbol == "O":
            self.start_ai_turn()

    def restart(self):
        game_logic.reset_board(self.board)

        self.current_player = self.selected_player
        self.ai_thinking = False

        if self.selected_player == "O":
            self.start_ai_turn()

    def start_ai_turn(self):
        self.ai_thinking = True
        self.ai_thinking_started = pygame.time.get_ticks()

    def update_score(self):
        winner = game_logic.check_winner(self.board)

        if winner:
            self.scores[winner] += 1

        elif game_logic.is_draw(self.board):
            self.scores["draws"] += 1

    def handle_human_move(self, position):
        if (
            not self.selected_player
            or self.ai_thinking
            or self.is_game_over()
            or not game_ui.BOARD_RECT.collidepoint(position)
        ):
            return

        mouse_x, mouse_y = position

        col = int(
            (mouse_x - settings.BOARD_X)
            // settings.CELL_SIZE
        )

        row = int(
            (mouse_y - settings.BOARD_Y)
            // settings.CELL_SIZE
        )

        if self.board[row][col] is not None:
            return

        self.board[row][col] = self.selected_player

        self.update_score()

        if not self.is_game_over():
            self.start_ai_turn()

    def handle_ai_move(self):
        ai_symbol = "O" if self.selected_player == "X" else "X"
        human_symbol = self.selected_player

        move = ai.get_best_move(
            self.board,
            ai_symbol,
            human_symbol
        )

        if move is None:
            return

        row, col = move
        self.board[row][col] = ai_symbol

        self.update_score()

    def handle_event(self, event):

        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if game_ui.RESTART_BUTTON.collidepoint(event.pos):
                self.restart()

            elif game_ui.X_BUTTON.collidepoint(event.pos):
                self.select_player("X")

            elif game_ui.O_BUTTON.collidepoint(event.pos):
                self.select_player("O")

            else:
                self.handle_human_move(event.pos)

    def update(self, current_time=None):

        if not self.ai_thinking:
            return

        if current_time is None:
            current_time = pygame.time.get_ticks()

        if (
            current_time - self.ai_thinking_started
            >= settings.AI_THINKING_DELAY
        ):
            self.handle_ai_move()
            self.ai_thinking = False

    def run(self):

        pygame.init()

        screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )

        pygame.display.set_caption(settings.WINDOW_TITLE)

        clock = pygame.time.Clock()

        fonts = {
            "title": pygame.font.Font(None, 38),
            "button": pygame.font.Font(None, 42),
            "status": pygame.font.Font(None, 28),
            "restart": pygame.font.Font(None, 24),
            "score": pygame.font.Font(None, 24)
        }

        while self.running:

            for event in pygame.event.get():
                self.handle_event(event)

            self.update()

            game_ui.draw_game(
                screen,
                fonts,
                self.board,
                self.scores,
                self.selected_player,
                self.current_player,
                self.ai_thinking
            )

            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
