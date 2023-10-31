from piecelogic import *
import random

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
        self.figure_dict = {" ": "", "♙": "", "♟": "", "♘": "N", "♞": "N", "♗": "B", "♝": "B", "♖": "R", "♜": "R",
                            "♕": "Q", "♛": "Q", "♔": "K", "♚": "K"}
        self.pieces_on_board = []
        self.pos_moves = set()
        for y in range(self.size):
            line = []
            for x in range(self.size):
                line.append(EmptyPiece())
            self.pieces_on_board.append(line)

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

    def make_a_move(self, figure_starting_coords, figure_resulting_coords):
        if self.move_verified(figure_starting_coords, figure_resulting_coords):

            current_piece_name = self.figure_dict[self.matrix[figure_starting_coords[0]][figure_starting_coords[1]]]
            takes = ""
            if self.matrix[figure_resulting_coords[0]][figure_resulting_coords[1]] != " ":
                takes = "x"
            starting_pos = ""
            decisive_change = ""  # mate check (later)

            if current_piece_name != "":
                starting_pos = str(figure_starting_coords[0] + 1) + self.alpha[figure_starting_coords[1]]
            resulting_pos = str(figure_resulting_coords[0] + 1) + self.alpha[figure_resulting_coords[1]]

            self.moves_played += current_piece_name + takes + starting_pos + resulting_pos + decisive_change + " "

            self.matrix[figure_resulting_coords[0]][figure_resulting_coords[1]] = \
                self.matrix[figure_starting_coords[0]][figure_starting_coords[1]]
            self.matrix[figure_starting_coords[0]][figure_starting_coords[1]] = ""
            return True
        else:
            return False


mtrx = Matrix(basic_matrix1)
# print(type(mtrx.pieces_on_board_dict["0 0"]))
print(mtrx.pieces_on_board[0][0].find_possible_moves(mtrx))
print(mtrx.pieces_on_board[3][2].find_possible_moves(mtrx))
print(mtrx.pieces_on_board[4][4].find_possible_moves(mtrx))
print(mtrx.pieces_on_board[2][5].find_possible_moves(mtrx))
print(mtrx.pieces_on_board[2][7].find_possible_moves(mtrx))
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
print(mtrx.collect_all_possible_moves())
print(mtrx.pick_a_move())
print(mtrx.collect_all_possible_moves("B"))
print(mtrx.pick_a_move())
