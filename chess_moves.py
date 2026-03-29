import argparse

PIECES = {"K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙",
          "k": "♚", "q": "♛", "r": "♜", "b": "♝", "n": "♞", "p": "♟"}

def parse_fen(fen):
    board = [[None]*8 for _ in range(8)]
    rows = fen.split("/")
    for r, row in enumerate(rows):
        c = 0
        for ch in row:
            if ch.isdigit(): c += int(ch)
            else: board[r][c] = ch; c += 1
    return board

def display(board):
    print("  a b c d e f g h")
    for r in range(8):
        row = f"{8-r} "
        for c in range(8):
            p = board[r][c]
            if p: row += PIECES.get(p, p) + " "
            else: row += ("·" if (r+c) % 2 == 0 else "·") + " "
        print(row + f"{8-r}")
    print("  a b c d e f g h")

def legal_moves(board, r, c):
    piece = board[r][c]
    if not piece: return []
    moves = []
    is_white = piece.isupper()
    def add(nr, nc):
        if 0 <= nr < 8 and 0 <= nc < 8:
            target = board[nr][nc]
            if target is None or target.isupper() != is_white:
                moves.append((nr, nc))
                return target is None
        return False
    p = piece.upper()
    if p == "P":
        d = -1 if is_white else 1
        if 0 <= r+d < 8 and board[r+d][c] is None: moves.append((r+d, c))
        for dc in [-1, 1]:
            if 0 <= r+d < 8 and 0 <= c+dc < 8:
                t = board[r+d][c+dc]
                if t and t.isupper() != is_white: moves.append((r+d, c+dc))
    elif p == "N":
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            add(r+dr, c+dc)
    elif p == "K":
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr or dc: add(r+dr, c+dc)
    else:
        dirs = []
        if p in "RQ": dirs += [(0,1),(0,-1),(1,0),(-1,0)]
        if p in "BQ": dirs += [(1,1),(1,-1),(-1,1),(-1,-1)]
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                t = board[nr][nc]
                if t is None: moves.append((nr, nc))
                else:
                    if t.isupper() != is_white: moves.append((nr, nc))
                    break
                nr += dr; nc += dc
    return moves

def sq(r, c): return chr(ord("a")+c) + str(8-r)

def main():
    p = argparse.ArgumentParser(description="Chess move validator")
    p.add_argument("--fen", default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    p.add_argument("--moves", help="Square to show moves for (e.g. e2)")
    p.add_argument("--display", action="store_true")
    args = p.parse_args()
    board = parse_fen(args.fen)
    if args.display or not args.moves: display(board)
    if args.moves:
        c = ord(args.moves[0]) - ord("a")
        r = 8 - int(args.moves[1])
        piece = board[r][c]
        if piece:
            mvs = legal_moves(board, r, c)
            print(f"{PIECES.get(piece, piece)} at {args.moves}: {', '.join(sq(mr,mc) for mr,mc in mvs)}")
        else:
            print(f"No piece at {args.moves}")

if __name__ == "__main__":
    main()
