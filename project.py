import random

# ---------------- Part 1: Board Initialization ----------------[BY SUHAS]

def add_new_tile(board):
    """Places a 2 (90%) or 4 (10%) in a random empty cell."""
    empty_cells = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                empty_cells.append((i, j))
    if not empty_cells:
        return
    i, j = random.choice(empty_cells)
    board[i][j] = 4 if random.random() < 0.1 else 2

def init_board():
    """Create a 4×4 board and add two random tiles (2 or 4)."""
    board = [[0 for _ in range(4)] for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board

# ---------------- Part 2: Movement Functions (Score Added!) ----------------[BY DISEN]

def compress(row):
    """Compress the row by sliding all non-zero elements to the left.
    Returns the new row and a boolean indicating if any change happened."""
    new_row = [num for num in row if num != 0]
    zeros = [0] * (len(row) - len(new_row))
    new_row += zeros
    changed = new_row != row
    return new_row, changed

def merge(row):
    """Merge the row by adding adjacent tiles of the same value.
    Returns new row, change status, and score gained."""
    changed = False
    score_gained = 0
    for i in range(len(row) - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            score_gained += row[i]
            row[i + 1] = 0
            changed = True
    return row, changed, score_gained

def move_left(board):
    """Move all tiles to the left with merge and compression.
    Returns (changed, score_gained_in_move)."""
    changed = False
    move_score = 0
    for i in range(4):
        new_row, compressed = compress(board[i])
        new_row, merged, score_gained = merge(new_row)
        move_score += score_gained
        new_row, _ = compress(new_row)
        if board[i] != new_row:
            changed = True
        board[i] = new_row
    return changed, move_score

def move_right(board):
    """Move all tiles to the right with merge and compression.
    Returns (changed, score_gained_in_move)."""
    changed = False
    move_score = 0
    for i in range(4):
        reversed_row = board[i][::-1]
        new_row, compressed = compress(reversed_row)
        new_row, merged, score_gained = merge(new_row)
        move_score += score_gained
        new_row, _ = compress(new_row)
        new_row = new_row[::-1]
        if board[i] != new_row:
            changed = True
        board[i] = new_row
    return changed, move_score

def transpose(board):
    """ HERE WE NEED TO TRANSPOSE AS UP AND DOWM FUNCTIONS ALSO NEED TO WORK"""
    return [list(row) for row in zip(*board)]

def move_up(board):
    transposed = transpose(board)
    changed, move_score = move_left(transposed)
    board[:] = transpose(transposed)
    return changed, move_score

def move_down(board):
    transposed = transpose(board)
    reversed=[row[::-1] for row in transposed]
    changed,move_score=move_right(reversed)
    board[:]=transpose(reversed)
    return changed,move_score


# ---------------- Part 3: User Interaction and Game Logic ----------------[BY SUSHEEL]

def game_cond(board):
    """Check game status:
    Return 1 if 2048 tile found (win),
    -1 if no moves possible (lose),
    0 if game should continue"""
    empty = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] == 2048:
                return 1  # Win
            if board[i][j] == 0:
                empty += 1
    if empty > 0:
        return 0  # Continue
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j + 1] or board[j][i] == board[j + 1][i]:
                return 0  # Moves possible
    return -1  # Lose

def num_span(board):
    """Spawn a new tile (2 or 4) in a random empty spot."""
    empty_places = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if not empty_places:
        return
    i, j = random.choice(empty_places)
    board[i][j] = 4 if random.random() < 0.1 else 2

def get_user_move(board):
    """Take user input, apply appropriate move, and return move_score."""
    while True:
        move = input("ENTER THE MOVE(w⬆️, a⬅️, s⬇️, d➡️): ").lower()
        if move == 'w':
            changed, move_score = move_up(board)
        elif move == 'a':
            changed, move_score = move_left(board)
        elif move == 's':
            changed, move_score = move_down(board)
        elif move == 'd':
            changed, move_score = move_right(board)
        else:
            print("Invalid move! Please enter w, a, s, or d.")
            continue
        if changed:
            num_span(board)
            return move_score
        else:
            print("Move didn't change the board, try a different move.")

def game_loop(board):
    """Main game loop: print board, user moves, check status."""
    score = 0
    while True:
        print_board(board)
        print(f"  SCORE: {score}  ")
        status = game_cond(board)
        if status == 1:
            print('🎉 YOU WON THE GAME 🎉')
            break
        elif status == -1:
            print('😭 Oops! YOU LOST THE GAME')
            break
        move_score = get_user_move(board)
        score += move_score

# ---------------- Part 4: Display and Colors ----------------(FOR COLOUR EFFECTS)[BY DHANUSH NARAYAN]

try:
    from colorama import Fore, Back, Style, init as colorama_init
    colorama_init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = False
    class Dummy:
        RESET_ALL = ""
        BRIGHT = ""
        DIM = ""
        WHITE = ""
        CYAN = ""
        GREEN = ""
        MAGENTA = ""
        YELLOW = ""
        RED = ""
        BLUE = ""
    Fore = Back = Style = Dummy()

COLOR_MAP = {
    0: Style.DIM,
    2: Fore.WHITE + Style.BRIGHT,
    4: Fore.CYAN + Style.BRIGHT,
    8: Fore.GREEN + Style.BRIGHT,
    16: Fore.MAGENTA + Style.BRIGHT,
    32: Fore.YELLOW + Style.BRIGHT,
    64: Fore.RED + Style.BRIGHT,
    128: Fore.WHITE + Back.BLUE + Style.BRIGHT,
    256: Fore.WHITE + Back.MAGENTA + Style.BRIGHT,
    512: Fore.WHITE + Back.GREEN + Style.BRIGHT,
    1024: Fore.WHITE + Back.YELLOW + Style.BRIGHT,
    2048: Fore.WHITE + Back.RED + Style.BRIGHT,
}

def color_tile(text, value):
    """Apply color formatting to a tile's text if colorama is available."""
    if not COLORS:
        return text
    return COLOR_MAP.get(value, Style.BRIGHT) + text + Style.RESET_ALL

def print_board(board):
    """Pretty print the board with colors and gridlines."""
    size = len(board)
    sep = "+" + ("------+" * size)
    print(sep)
    for row in board:
        line = "|"
        for val in row:
            text = str(val) if val != 0 else ""
            formatted = f"{text:^6}"
            colored = color_tile(formatted, val)
            line += colored + "|"
        print(line)
        print(sep)

# ---------------- Main Script Start ----------------

if __name__ == "__main__":
    board = init_board()
    game_loop(board)
