from piecelogic import *

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


class Matrix:
    def __init__(self, matrix=None):
        if matrix is None:
            matrix = basic_matrix

        self.matrix = matrix
        self.moves_played = ""
        self.alpha = "abcdefgh"
        self.figure_dict = {" ": "", "♙": "", "♟": "", "♘": "N", "♞": "N", "♗": "B", "♝": "B", "♖": "R", "♜": "R", "♕": "Q", "♛": "Q", "♔": "K", "♚": "K"}
        self.pieces_on_board_dict = {}
        for y in range(8):
            for x in range(8):
                match self.matrix[y][x]:
                    case " ", "":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = " "
                    case "♙":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = Pawn(y, x, "W")
                    case "♟":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = Pawn(y, x, "B")
                    case "♘":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = Knight(y, x, "W")
                    case "♞":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = Knight(y, x, "B")
                    case "♗":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = Bishop(y, x, "W")
                    case "♝":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = Bishop(y, x, "B")
                    case "♖":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = Rook(y, x, "W")
                    case "♜":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = Rook(y, x, "B")
                    case "♕":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = Queen(y, x, "W")
                    case "♛":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = Queen(y, x, "B")
                    case "♔":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = King(y, x, "W")
                    case "♚":
                        self.pieces_on_board_dict[str(y) + " " + str(x)] = King(y, x, "B")

    def move_verified(self, figure_starting_coords, figure_resulting_coords):
        # verifying logic here
        return True

    def possible_moves(self, piece_coords):
        pass

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

            self.matrix[figure_resulting_coords[0]][figure_resulting_coords[1]] = self.matrix[figure_starting_coords[0]][figure_starting_coords[1]]
            self.matrix[figure_starting_coords[0]][figure_starting_coords[1]] = ""
            return True
        else:
            return False
