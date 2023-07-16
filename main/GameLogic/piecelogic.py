class Piece:
    def __init__(self, y, x, color):  # 0-7:0-7:W/B
        self.cost = 0
        self.y = y
        self.x = x
        self.color = color
        self.symbol = "X"

    def movement_logic(self, matrix):
        moves = []
        move = (self.y, self.x)
        moves.append(move)
        return moves

    def find_possible_moves(self, matrix):
        moves_set = self.movement_logic(matrix)
        return moves_set


class Pawn(Piece):

    def __init__(self, y, x, color):
        super().__init__(y, x, color)
        self.cost = 1
        self.symbol = "♙" if color == "W" else "♟"

    def movement_logic(self, matrix):
        moves = []
        move = (self.x, self.y)  # переписать
        moves.append(move)
        return moves


class Rook(Piece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color)
        self.cost = 1
        self.symbol = "♖" if color == "W" else "♜"

    def movement_logic(self, matrix):
        moves = []
        move = (self.x, self.y)  # переписать
        moves.append(move)
        return moves


class Knight(Piece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color)
        self.cost = 3
        self.symbol = "♘" if color == "W" else "♞"

    def movement_logic(self, matrix):
        moves = []
        move = (self.x, self.y)  # переписать
        moves.append(move)
        return moves


class Bishop(Piece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color)
        self.cost = 3
        self.symbol = "♗" if color == "W" else "♝"

    def movement_logic(self, matrix):
        moves = []
        move = (self.x, self.y)  # переписать
        moves.append(move)
        return moves


class Queen(Piece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color)
        self.cost = 9
        self.symbol = "♕" if color == "W" else "♛"

    def movement_logic(self, matrix):
        moves = []
        move = (self.x, self.y)  # переписать
        moves.append(move)
        return moves


class King(Piece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color)
        self.cost = 69
        self.symbol = "♔" if color == "W" else "♚"

    def find_attacked_squares(self, matrix):
        attacked_squares = []
        for i in range(8):
            attacked_squares.append([False for i in range(8)])
        # logic
        return attacked_squares

    def movement_logic(self, matrix):
        moves = []
        move = (self.x, self.y)  # переписать
        moves.append(move)
        return moves


P = Pawn(2, 1, "W")

print(P.find_possible_moves(1))
