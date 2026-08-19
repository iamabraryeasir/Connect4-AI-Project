ROW_COUNT = 6
COLUMN_COUNT = 7


def dfs_directional(board, row, col, piece, dr, dc, explored, ui_callback=None):
    next_row = row + dr
    next_col = col + dc

    if (
        next_row < 0
        or next_row >= ROW_COUNT
        or next_col < 0
        or next_col >= COLUMN_COUNT
    ):
        return 0, []

    explored.add((next_row, next_col))
    if ui_callback:
        ui_callback(next_row, next_col, explored)

    if board[next_row][next_col] != piece:
        return 0, []

    count, path = dfs_directional(
        board, next_row, next_col, piece, dr, dc, explored, ui_callback
    )
    return 1 + count, [(next_row, next_col)] + path


def check_win(board, piece, last_row=None, last_col=None, ui_callback=None):
    if last_row is None or last_col is None:
        return check_win_full(board, piece, ui_callback)

    explored = set()
    explored.add((last_row, last_col))

    if ui_callback:
        ui_callback(last_row, last_col, explored)

    axes = [
        ((0, 1), (0, -1)),
        ((1, 0), (-1, 0)),
        ((1, 1), (-1, -1)),
        ((1, -1), (-1, 1)),
    ]

    for (dr1, dc1), (dr2, dc2) in axes:
        count1, path1 = dfs_directional(
            board, last_row, last_col, piece, dr1, dc1, explored, ui_callback
        )
        count2, path2 = dfs_directional(
            board, last_row, last_col, piece, dr2, dc2, explored, ui_callback
        )

        if 1 + count1 + count2 >= 4:
            win_path = path2[::-1] + [(last_row, last_col)] + path1
            return True, win_path, explored

    return False, [], explored


def check_win_full(board, piece, ui_callback=None):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece:
                is_win, path, explored = check_win(board, piece, r, c, ui_callback)
                if is_win:
                    return True, path, explored
    return False, [], set()
