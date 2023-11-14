def coordinates_possibility_sub_check(matrix, y, x):
    if max(x, y) >= matrix.size or min(x, y) < 0:
        return 0
    return 1


class EmptyPiece:
    alpha = 'ABCDEFGH'

    def __init__(self, y=0, x=0, color="W"):  # 0-7:0-7:W/B
        self.cost = 0
        self.y = y
        self.x = x
        self.color = color
        self.symbol = "X"
        self.pos_moves = set()
        self.move_types = []
        self.moved = 0

    def find_possible_moves(self, matrix):
        # Function calls each movement type checker that this piece has
        self.pos_moves.clear()
        for move_type in self.move_types:
            move_type(matrix)

        return self.pos_moves

    def linear_continuity_sub_check(self, matrix, y, x):
        # Function determines if it's possible to move to that specific
        # square and whether you should try checking next one
        if coordinates_possibility_sub_check(matrix, y, x) == 0:
            return -1
        if type(matrix.pieces_on_board[y][x]) == EmptyPiece:
            self.pos_moves.add(self.alpha[x] + str(y + 1))
            print("y: ", y, " x: ", x)
            return 1
        if matrix.pieces_on_board[y][x].color != matrix.pieces_on_board[self.y][self.x].color:
            self.pos_moves.add(self.alpha[x] + str(y + 1))
            print("y: ", y, " x: ", x)
        return 0

    def linear_continuity_pawn_sub_check(self, matrix, y, x):
        # Function determines if it's possible to move to that specific
        # square for a pawn and whether you should try checking next one
        if coordinates_possibility_sub_check(matrix, y, x) == 0:
            return -1
        if type(matrix.pieces_on_board[y][x]) == EmptyPiece:
            return 0
        if matrix.pieces_on_board[y][x].color != matrix.pieces_on_board[self.y][self.x].color:
            self.pos_moves.add(self.alpha[x] + str(y + 1))
        return 0

    def linear_continuity_no_take_sub_check(self, matrix, y, x):
        # Same to previous but without taking the piece on the last possible square
        if coordinates_possibility_sub_check(matrix, y, x) == 0:
            return -1
        if type(matrix.pieces_on_board[y][x]) == EmptyPiece:
            self.pos_moves.add(self.alpha[x] + str(y + 1))
            return 1
        return 0

    def first_piece_to_the_left(self, matrix):
        for x in range(self.x - 1, -1, -1):
            if type(matrix.pieces_on_board[self.y][x]) != EmptyPiece:
                return matrix.pieces_on_board[self.y][x]
        return EmptyPiece()

    def first_piece_to_the_right(self, matrix):
        for x in range(self.x + 1, matrix.size):
            if type(matrix.pieces_on_board[self.y][x]) != EmptyPiece:
                return matrix.pieces_on_board[self.y][x]
        return EmptyPiece()

    def horizontal_check(self, matrix):
        # Function generates all horizontal coordinates moving away from the piece and checks them
        print("here1")
        for x in range(self.x + 1, matrix.size):
            print("here2")
            res = self.linear_continuity_sub_check(matrix, self.y, x)
            if res == 0:
                break

        for x in range(self.x - 1, -1, -1):
            print("here3")
            res = self.linear_continuity_sub_check(matrix, self.y, x)
            if res == 0:
                break
        return 1

    def vertical_check(self, matrix):
        # Function generates all vertical coordinates moving away from the piece and checks them
        for y in range(self.y + 1, len(matrix.matrix)):
            if self.linear_continuity_sub_check(matrix, y, self.x) == 0:
                break

        for y in range(self.y - 1, -1, -1):
            if self.linear_continuity_sub_check(matrix, y, self.x) == 0:
                break
        return 1

    def diagonal_check(self, matrix):
        # Function generates all diagonal coordinates in order of moving away from the piece and checks them
        for add in range(1, min(self.y, self.x) + 1):
            if not self.linear_continuity_sub_check(matrix, self.y - add, self.x - add):
                break
        for add in range(1, min(matrix.size - self.y, matrix.size - self.x) + 1):
            if not self.linear_continuity_sub_check(matrix, self.y + add, self.x + add):
                break
        for add in range(1, min(matrix.size - self.y, self.x) + 1):
            if not self.linear_continuity_sub_check(matrix, self.y + add, self.x - add):
                break
        for add in range(1, min(self.y, matrix.size - self.x) + 1):
            if not self.linear_continuity_sub_check(matrix, self.y - add, self.x + add):
                break
        return 1

    def knight_check(self, matrix):
        # Checks for all possible knight moves
        moveset = [[1, 2], [-1, -2], [2, 1], [-2, 1], [1, -2], [-1, 2], [2, -1], [-2, -1]]
        for y, x in moveset:
            self.linear_continuity_sub_check(matrix, self.y + y, self.x + x)
        return 1

    def king_check(self, matrix):
        # Checks for all possible king moves
        moveset = [[1, 1], [-1, -1], [-1, 1], [1, -1], [0, 1], [0, -1], [1, 0], [-1, 0]]
        for y, x in moveset:
            self.linear_continuity_sub_check(matrix, self.y + y, self.x + x)
        return 1

    def pawn_check(self, matrix):
        # Checks for all possible pawn moves
        # Overridden by Pawn class due to movement specifications
        pass

    def castle(self, matrix):
        if type(self) == King and not self.moved:
            left_figure = self.first_piece_to_the_left(matrix)
            right_figure = self.first_piece_to_the_right(matrix)
            if type(left_figure) == Rook and not left_figure.moved:
                self.pos_moves.add("0-0")
            if type(right_figure) == Rook and not right_figure.moved:
                self.pos_moves.add("0-0-0")


class Pawn(EmptyPiece):

    def __init__(self, y, x, color):
        super().__init__(y, x, color)
        self.cost = 1
        self.symbol = "♙" if color == "W" else "♟"
        self.move_types = [self.pawn_check]

    def pawn_check(self, matrix):
        # Function that checks for all possible pawn moves
        # Overridden from the mother-class
        y_add, x_add = -1, 0
        if self.color == "B":
            y_add *= -1
        res = self.linear_continuity_no_take_sub_check(matrix, self.y + y_add, self.x + x_add)
        if not self.moved and res and (self.y == 6 or self.y == 1):
            self.linear_continuity_no_take_sub_check(matrix, self.y + y_add * 2, self.x + x_add)

        take_moveset = [[-1, -1], [-1, 1]]
        if self.color == "B":
            for move in take_moveset:
                move[0] *= -1

        for y, x in take_moveset:
            self.linear_continuity_pawn_sub_check(matrix, self.y + y, self.x + x)


class Rook(EmptyPiece):

    def __init__(self, y, x, color):
        super().__init__(y, x, color)
        self.cost = 5
        self.symbol = "♖" if color == "W" else "♜"
        self.move_types = [self.vertical_check, self.horizontal_check]


class Knight(EmptyPiece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color)
        self.cost = 3
        self.symbol = "♘" if color == "W" else "♞"
        self.move_types = [self.knight_check]


class Bishop(EmptyPiece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color)
        self.cost = 3
        self.symbol = "♗" if color == "W" else "♝"
        self.move_types = [self.diagonal_check]


class Queen(EmptyPiece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color)
        self.cost = 9
        self.symbol = "♕" if color == "W" else "♛"
        self.move_types = [self.vertical_check, self.horizontal_check, self.diagonal_check]


class King(EmptyPiece):
    def __init__(self, y, x, color):
        super().__init__(y, x, color)
        self.cost = 69
        self.symbol = "♔" if color == "W" else "♚"
        self.move_types = [self.king_check, self.castle]

# P = Pawn(2, 1, "W")
# R = Rook(3, 3, "W")
# print(R.find_possible_moves())
# print(P.find_possible_moves(1))
