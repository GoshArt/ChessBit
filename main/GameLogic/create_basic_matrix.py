from main.GameLogic.piecelogic import *
import random

basic_matrix2D = "rnbqkbnrpppppppp11111111111111111111111111111111PPPPPPPPRNBQKBNR0000000000000000000000000000000000000000000000000000000000000000"

basic_matrix = [
    ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],  # 8
    ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],  # 7
    [" ", " ", " ", " ", " ", " ", " ", " "],  # 6
    [" ", " ", " ", " ", " ", " ", " ", " "],  # 5
    [" ", " ", " ", " ", " ", " ", " ", " "],  # 4
    [" ", " ", " ", " ", " ", " ", " ", " "],  # 3
    ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],  # 2
    ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"],  # 1
]  # a     b     c    d     e     f    g     h

basic_matrix1 = [
    ["♜", " ", "", "", "", "", "", ""],  # 8
    [" ", "", "", "", "", "", "♟", "♟"],  # 7
    [" ", " ", " ", " ", " ", "♙", " ", "♔"],  # 6
    [" ", " ", "♝", " ", " ", " ", " ", " "],  # 5
    [" ", " ", " ", " ", "♘", " ", " ", " "],  # 4
    [" ", " ", " ", " ", " ", " ", " ", " "],  # 3
    ["", "", "", "", "", "", "", ""],  # 2
    ["", "", "", "", "", "", "", ""],  # 1
]  # a     b     c    d     e     f    g     h


class Matrix:

    def __init__(self, matrix=None):
        if matrix is None:
            matrix = basic_matrix

        self.size = 8
        self.matrix = matrix
        self.moves_played = ""
        self.alpha = "ABCDEFGH"
        self.alpha_to_num = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8}
        self.figure_dict = {" ": "", "♙": "", "♟": "", "♘": "N", "♞": "N", "♗": "B", "♝": "B", "♖": "R", "♜": "R",
                            "♕": "Q", "♛": "Q", "♔": "K", "♚": "K"}
        self.pieces_on_board = []
        self.pos_moves = set()
        self.stringified_pieces = {EmptyPiece: {"B": "1", "W": "1"}, Rook: {"B": "r", "W": "R"},
                                   Knight: {"B": "n", "W": "N"}, Bishop: {"B": "b", "W": "B"},
                                   Queen: {"B": "q", "W": "Q"}, King: {"B": "k", "W": "K"},
                                   Pawn: {"B": "p", "W": "P"}}
        for y in range(self.size):
            line = []
            for x in range(self.size):
                line.append(EmptyPiece())
            self.pieces_on_board.append(line)

        if len(matrix[0]) == 1:
            for item in range(0, 64):
                y = item // self.size
                x = item % self.size
                match self.matrix[item]:
                    case "1":
                        self.pieces_on_board[y][x] = EmptyPiece()
                    case "r":
                        self.pieces_on_board[y][x] = Rook(y, x, "B")
                    case "n":
                        self.pieces_on_board[y][x] = Knight(y, x, "B")
                    case "b":
                        self.pieces_on_board[y][x] = Bishop(y, x, "B")
                    case "q":
                        self.pieces_on_board[y][x] = Queen(y, x, "B")
                    case "k":
                        self.pieces_on_board[y][x] = King(y, x, "B")
                    case "p":
                        self.pieces_on_board[y][x] = Pawn(y, x, "B")
                    case "R":
                        self.pieces_on_board[y][x] = Rook(y, x, "W")
                    case "N":
                        self.pieces_on_board[y][x] = Knight(y, x, "W")
                    case "B":
                        self.pieces_on_board[y][x] = Bishop(y, x, "W")
                    case "Q":
                        self.pieces_on_board[y][x] = Queen(y, x, "W")
                    case "K":
                        self.pieces_on_board[y][x] = King(y, x, "W")
                    case "P":
                        self.pieces_on_board[y][x] = Pawn(y, x, "W")
        else:
            for y in range(self.size):
                for x in range(self.size):
                    match self.matrix[y][x]:
                        case " ", "":
                            self.pieces_on_board[y][x] = EmptyPiece()
                        case "♙":
                            self.pieces_on_board[y][x] = Pawn(y, x, "W")
                        case "♟":
                            self.pieces_on_board[y][x] = Pawn(y, x, "B")
                        case "♘":
                            self.pieces_on_board[y][x] = Knight(y, x, "W")
                        case "♞":
                            self.pieces_on_board[y][x] = Knight(y, x, "B")
                        case "♗":
                            self.pieces_on_board[y][x] = Bishop(y, x, "W")
                        case "♝":
                            self.pieces_on_board[y][x] = Bishop(y, x, "B")
                        case "♖":
                            self.pieces_on_board[y][x] = Rook(y, x, "W")
                        case "♜":
                            self.pieces_on_board[y][x] = Rook(y, x, "B")
                        case "♕":
                            self.pieces_on_board[y][x] = Queen(y, x, "W")
                        case "♛":
                            self.pieces_on_board[y][x] = Queen(y, x, "B")
                        case "♔":
                            self.pieces_on_board[y][x] = King(y, x, "W")
                        case "♚":
                            self.pieces_on_board[y][x] = King(y, x, "B")

    def move_verified(self, figure_starting_coords, figure_resulting_coords):
        # verifying logic here
        # implemented on front-end
        return True

    def pick_a_move(self):
        return random.choice(list(self.pos_moves))

    def collect_all_possible_moves(self, color="W"):
        # Function calls methods for every piece of given color and collects all possible moves
        self.pos_moves.clear()
        for y in range(self.size):
            for x in range(self.size):
                if type(self.pieces_on_board[y][x]) != EmptyPiece and self.pieces_on_board[y][x].color == color:
                    self.pieces_on_board[y][x].find_possible_moves(self)
                    for move in self.pieces_on_board[y][x].pos_moves:
                        self.pos_moves.add(str(self.alpha[x]) + str(y + 1) + "->" + move)
        return self.pos_moves

    def make_a_move(self, move_str):
        x1 = self.alpha_to_num[move_str[0]]
        y1 = int(move_str[1])
        x2 = self.alpha_to_num[move_str[4]]
        y2 = int(move_str[5])
        self.pieces_on_board[y2 - 1][x2 - 1] = self.pieces_on_board[y1 - 1][x1 - 1]
        self.pieces_on_board[y1 - 1][x1 - 1] = EmptyPiece()

    def matrix_to_string_conversion(self):
        result = ""
        for y in range(self.size):
            for x in range(self.size):
                color = self.pieces_on_board[y][x].color
                result += self.stringified_pieces[type(self.pieces_on_board[y][x])][color]
        return result + "0" * 64


# mtrx = Matrix(basic_matrix2D)
# print(mtrx.matrix_to_string_conversion())
# print(type(mtrx.pieces_on_board_dict["0 0"]))
# print(mtrx.pieces_on_board[0][0].find_possible_moves(mtrx))
# print(mtrx.pieces_on_board[3][2].find_possible_moves(mtrx))
# print(mtrx.pieces_on_board[4][4].find_possible_moves(mtrx))

# print(mtrx.pieces_on_board[2][5].find_possible_moves(mtrx))
# print(mtrx.pieces_on_board[2][7].find_possible_moves(mtrx))
# basic_matrix1 = [
#     ["♜", " ", "", "", "", "", "", ""],  # 8
#     [" ", "", "", "", "", "", "♟", "♟"],  # 7
#     [" ", " ", " ", " ", " ", "♙", " ", "♔"],  # 6
#     [" ", " ", "♝", " ", " ", " ", " ", " "],  # 5
#     [" ", " ", " ", " ", "♘", " ", " ", " "],  # 4
#     [" ", " ", " ", " ", " ", " ", " ", " "],  # 3
#     ["", "", "", "", "", "", "", ""],  # 2
#     ["", "", "", "", "", "", "", ""],  # 1
# ]  # a     b     c    d     e     f    g     h
# print(mtrx.collect_all_possible_moves())
# print(mtrx.pick_a_move())
# print(mtrx.collect_all_possible_moves("B"))
# print(mtrx.pick_a_move())
# mtrx = Matrix(basic_matrix2D)
# print(mtrx.collect_all_possible_moves("B"))
# print(mtrx.matrix_to_string_conversion())
# mtrx.make_a_move(mtrx.pick_a_move())
# print(mtrx.matrix_to_string_conversion())
# print("DONE")
# mtrx.pieces_on_board[0][0] = mtrx.pieces_on_board[0][1]
# mtrx.pieces_on_board[0][1] = EmptyPiece()
# print(1)
