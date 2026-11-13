def check_winner(board):
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


def is_draw(board):
    return all(
        cell is not None
        for row in board
        for cell in row
    )


def reset_board(board):
    for row in board:
        row[:] = [None, None, None]


def switch_player(current_player):
    return "O" if current_player == "X" else "X"
