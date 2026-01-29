import random

# Directions for neighboring cells
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1),  (1, 0),  (1, 1)]

def create_board(rows, cols, mines):
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_positions = set()

    while len(mine_positions) < mines:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        mine_positions.add((r, c))

    for r, c in mine_positions:
        board[r][c] = "M"
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "M":
                board[nr][nc] += 1

    return board, mine_positions

def print_board(visible):
    print("\n   " + " ".join(str(i) for i in range(len(visible[0]))))
    print("  " + "-" * (2 * len(visible[0]) - 1))
    for i, row in enumerate(visible):
        print(f"{i} |" + " ".join(row))

def reveal(board, visible, r, c, visited):
    if (r, c) in visited:
        return
    visited.add((r, c))

    if board[r][c] == 0:
        visible[r][c] = " "
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
                reveal(board, visible, nr, nc, visited)
    else:
        visible[r][c] = str(board[r][c])

def play_minesweeper(rows=8, cols=8, mines=10):
    board, mine_positions = create_board(rows, cols, mines)
    visible = [["■" for _ in range(cols)] for _ in range(rows)]
    flags = set()
    revealed = set()

    while True:
        print_board(visible)
        move = input("\nEnter move (r c) or flag (f r c): ").split()

        if not move:
            continue

        if move[0] == "f":
            r, c = int(move[1]), int(move[2])
            if visible[r][c] == "■":
                visible[r][c] = "F"
                flags.add((r, c))
            elif visible[r][c] == "F":
                visible[r][c] = "■"
                flags.remove((r, c))
            continue

        r, c = map(int, move)

        if (r, c) in mine_positions:
            print("\n💥 BOOM! You hit a mine!")
            for mr, mc in mine_positions:
                visible[mr][mc] = "M"
            print_board(visible)
            return

        reveal(board, visible, r, c, revealed)

        # Win condition
        safe_cells = rows * cols - mines
        revealed_count = sum(
            1 for r in range(rows) for c in range(cols)
            if visible[r][c] != "■" and visible[r][c] != "F"
        )

        if revealed_count == safe_cells:
            print("\n🎉 You win! All safe cells revealed.")
            print_board(visible)
            return

if __name__ == "__main__":
    play_minesweeper()
