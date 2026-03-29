#!/usr/bin/env python3
"""Chess move generator and board representation."""
import sys

PIECES = {"K": "king", "Q": "queen", "R": "rook", "B": "bishop", "N": "knight", "P": "pawn"}

class Board:
    def __init__(self):
        self.squares = {}
        self._setup()
    def _setup(self):
        order = "RNBQKBNR"
        for c in range(8):
            self.squares[(0, c)] = ("w", order[c])
            self.squares[(1, c)] = ("w", "P")
            self.squares[(6, c)] = ("b", "P")
            self.squares[(7, c)] = ("b", order[c])
    def get(self, r, c):
        return self.squares.get((r, c))
    def moves(self, r, c):
        piece = self.get(r, c)
        if not piece: return []
        color, ptype = piece
        result = []
        if ptype == "P":
            d = 1 if color == "w" else -1
            if 0 <= r+d < 8 and not self.get(r+d, c):
                result.append((r+d, c))
                start_row = 1 if color == "w" else 6
                if r == start_row and not self.get(r+2*d, c):
                    result.append((r+2*d, c))
            for dc in (-1, 1):
                if 0 <= r+d < 8 and 0 <= c+dc < 8:
                    target = self.get(r+d, c+dc)
                    if target and target[0] != color:
                        result.append((r+d, c+dc))
        elif ptype == "N":
            for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < 8 and 0 <= nc < 8:
                    target = self.get(nr, nc)
                    if not target or target[0] != color:
                        result.append((nr, nc))
        elif ptype in ("R", "Q", "B", "K"):
            dirs = []
            if ptype in ("R", "Q"): dirs += [(0,1),(0,-1),(1,0),(-1,0)]
            if ptype in ("B", "Q"): dirs += [(1,1),(1,-1),(-1,1),(-1,-1)]
            if ptype == "K": dirs = [(dr,dc) for dr in (-1,0,1) for dc in (-1,0,1) if (dr,dc)!=(0,0)]
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    target = self.get(nr, nc)
                    if target:
                        if target[0] != color: result.append((nr, nc))
                        break
                    result.append((nr, nc))
                    if ptype == "K": break
                    nr += dr; nc += dc
        return result
    def to_string(self):
        lines = []
        for r in range(7, -1, -1):
            row = f"{r+1} "
            for c in range(8):
                p = self.get(r, c)
                if p:
                    ch = p[1] if p[0] == "w" else p[1].lower()
                    row += ch + " "
                else:
                    row += ". "
            lines.append(row)
        lines.append("  a b c d e f g h")
        return chr(10).join(lines)

def test():
    b = Board()
    assert b.get(0, 0) == ("w", "R")
    assert b.get(7, 4) == ("b", "K")
    # Pawn moves from starting position
    moves = b.moves(1, 4)  # e2 pawn
    assert (2, 4) in moves and (3, 4) in moves
    assert len(moves) == 2
    # Knight moves
    moves = b.moves(0, 1)  # b1 knight
    assert (2, 0) in moves and (2, 2) in moves
    assert len(moves) == 2
    s = b.to_string()
    assert "R" in s
    print("  chess_moves: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print(Board().to_string())
