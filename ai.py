import game_logic

def minimax(board, ai_symbol, human_symbol, is_maximizing, depth=0):

    winner = game_logic.check_winner(board)

    if winner == ai_symbol:
        return 10 - depth

    if winner == human_symbol:
        return depth - 10

    if game_logic.is_draw(board):
        return 0

    best_score = float("-inf") if is_maximizing else float("inf")

    for row in range(3):
        for col in range(3):

            if board[row][col] is None:

                if is_maximizing:
                    board[row][col] = ai_symbol

                    score = minimax(
                        board,
                        ai_symbol,
                        human_symbol,
                        False,
                        depth + 1
                    )

                    best_score = max(best_score, score)

                else:
                    board[row][col] = human_symbol

                    score = minimax(
                        board,
                        ai_symbol,
                        human_symbol,
                        True,
                        depth + 1
                    )

                    best_score = min(best_score, score)

                board[row][col] = None

    return best_score


def get_best_move(board, ai_symbol, human_symbol):

    best_score = float("-inf")
    best_move = None

    for row in range(3):
        for col in range(3):

            if board[row][col] is None:

                board[row][col] = ai_symbol

                score = minimax(
                    board,
                    ai_symbol,
                    human_symbol,
                    False
                )

                board[row][col] = None

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move
