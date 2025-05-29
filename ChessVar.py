# Author: Kevin Penate
# GitHub username: Ronniekev
# Date: 6/4/2024
# Description: Builds an atomic chess game board, that allows two players to move pieces and will return the winner
# of the game. Has helper functions that calculate the moves a piece can make and returns a list of valid moves.


def bishop_helper(chess_board, temp, temp_row, temp_help, row_help, capture_list, list1, bishop_list):
    """returns a list of valid moves for a bishop piece"""
    for x in range(9):
        if 0 < temp < 9 and 0 < temp_row < 9:
            if chess_board[temp_row][temp] in list1:
                break
            elif chess_board[temp_row][temp] == ".":
                bishop_list.append([temp_row, temp])
            elif chess_board[temp_row][temp] in capture_list:
                bishop_list.append([temp_row, temp])
                break
        temp_row = temp_row + row_help
        temp = temp + temp_help
    return


def knight_helper(chess_board, temp_column, temp_row, knight_list, capture_list, list1):
    """returns a list of valid moves for a bishop piece"""

    if 0 < temp_column < 9 and 0 < temp_row < 9:
        if chess_board[temp_row][temp_column] in list1:
            pass
        elif chess_board[temp_row][temp_column] == ".":
            knight_list.append([temp_row, temp_column])
        elif chess_board[temp_row][temp_column] in capture_list:
            knight_list.append([temp_row, temp_column])
    return


def rook_helper(chess_board, temp_column, temp_row, row_help, column_help, capture_list, list1, rook_list):
    """returns a list of valid moves for a rook piece"""

    for x in range(9):
        if 0 < temp_column < 9 and 0 < temp_row < 9 and chess_board[temp_row][temp_column] not in list1:
            if chess_board[temp_row][temp_column] == ".":
                rook_list.append([temp_row, temp_column])

            if chess_board[temp_row][temp_column] in capture_list:
                rook_list.append([temp_row, temp_column])
                break
            temp_row = temp_row + row_help
            temp_column = temp_column + column_help
    return


def king_helper(chess_board, temp_column, temp_row, king_list):
    """returns a list of valid moves for a king piece"""
    if 0 < temp_column < 9 and 0 < temp_row < 9:
        if chess_board[temp_row][temp_column] == ".":
            king_list.append([temp_row, temp_column])
            return


def is_move_valid(move_to, move_list):
    """returns True if a move is valid and False if it not"""

    if move_to in move_list:
        return True
    else:
        return False


def king_check_help(chess_board, temp_column, temp_row, king_check):
    """helps create a list of chess pieces to determine if an explosion can proceed"""

    if 0 < temp_column < 9 and 0 < temp_row < 9:
        king_check.append(chess_board[temp_row][temp_column])
    return


class ChessVar:
    """creates a game of chess"""

    def __init__(self):
        """takes no parameters, initializes a Chessboard and the player turn variable the ChessVariation"""
        self._board = [[" ", "a", "b", "c", "d", "e", "f", "g", "h", " "],
                       ["8", "R", "N", "B", "Q", "K", "B", "N", "R", "8"],
                       ["7", "P", "P", "P", "P", "P", "P", "P", "P", "7"],
                       ["6", ".", ".", ".", ".", ".", ".", ".", ".", "6"],
                       ["5", ".", ".", ".", ".", ".", ".", ".", ".", "5"],
                       ["4", ".", ".", ".", ".", ".", ".", ".", ".", "4"],
                       ["3", ".", ".", ".", ".", ".", ".", ".", ".", "3"],
                       ["2", "p", "p", "p", "p", "p", "p", "p", "p", "2"],
                       ["1", "r", "n", "b", "q", "k", "b", "n", "r", "1"],
                       [" ", "a", "b", "c", "d", "e", "f", "g", "h", " "]]
        self._player_turn = 0
        self._black_pieces = ["R", "N", "B", "Q", "K", "P"]
        self._white_pieces = ["q", "k", "b", "n", "r", "p"]

    def make_move(self, move_from, move_to):
        """receives string parameters for board locations, to move a piece from and to,if the move is valid
        the board will reflect the change"""

        status = self.get_game_state()
        if status != "UNFINISHED":
            return False

        player = self.player_turn()
        valid_moves = self.list_of_moves(move_from, player)
        move_from = self.get_location(move_from)
        move_to = self.get_location(move_to)

        is_valid = is_move_valid(move_to, valid_moves)
        if is_valid:
            if self._board[move_to[0]][move_to[1]] == ".":
                self._board[move_to[0]][move_to[1]] = self._board[move_from[0]][move_from[1]]
                self._board[move_from[0]][move_from[1]] = "."
                self._player_turn += 1
                return True

            elif self.explosion(move_to) is False:
                return False
            else:
                self.explosion(move_to)
                self._board[move_from[0]][move_from[1]] = "."
                self._board[move_to[0]][move_to[1]] = "."  # the piece captured and the capturing piece are removed
                self._player_turn += 1
                return True

        else:

            return False

    def get_game_state(self):
        """returns status of the game"""
        check_game = self._white_pieces + self._black_pieces

        if "k" in check_game and "K" in check_game:
            return "UNFINISHED"
        elif "k" in check_game:
            return "WHITE_WON"
        else:
            return "BLACK_WON"

    def explosion(self, move):
        """takes a move and updates the board to reflect an explosion if a capture is made"""
        column = move[1]
        row = move[0]
        king_check = []
        values = [-1, 1]

        for value in values:
            king_check_help(self._board, column, row + value, king_check)
            king_check_help(self._board, column + value, row, king_check)
            king_check_help(self._board, column + value, row - 1, king_check)
            king_check_help(self._board, column + value, row + 1, king_check)

        if "K" in king_check and "k" in king_check:
            return False  # confirms there are not two consecutive kings

        for value in values:
            self.explosion_helper(column + value, row - 1)
            self.explosion_helper(column + value, row + 1)
            self.explosion_helper(column, row + value)
            self.explosion_helper(column + value, row)

        return

    def explosion_helper(self, temp_column, temp_row):
        """helps sort through an explosion and removes pieces as needed"""
        if 0 < temp_column < 9 and 0 < temp_row < 9:
            if self._board[temp_row][temp_column] != "p" or self._board[temp_row][temp_column] != "P":
                self.remove_king(temp_column, temp_row)

    def remove_king(self, column, row):
        """checks to see if a king should be removed and the game updated to appropriate winner"""
        if self._board[row][column] == "k":
            self._white_pieces.remove('k')
            self.get_game_state()

        elif self._board[row][column] == "K":
            self._white_pieces.remove('k')
            self.get_game_state()
        self._board[row][column] = "."
        return

    def print_board(self):
        """prints the current chess board"""
        for row in self._board:
            print(*row)

    def player_turn(self):
        """returns the players color of who's turn it is. Even numbers will be white turn, odd numbers
        will indicate black turn"""

        if self._player_turn % 2 == 0:
            return "white"
        else:
            return "black"

    def get_location(self, move):
        """returns int variable for index location of pieces, if the location is not on the board it will return
        False"""
        location = []
        if move[1] == "8":
            location.append(1)
        elif move[1] == "7":
            location.append(2)
        elif move[1] == "6":
            location.append(3)
        elif move[1] == "5":
            location.append(4)
        elif move[1] == "4":
            location.append(5)
        elif move[1] == "3":
            location.append(6)
        elif move[1] == "2":
            location.append(7)
        elif move[1] == "1":
            location.append(8)
        else:
            return []

        for value in self._board[0]:
            if value == move[0]:
                location.append(self._board[0].index(move[0]))
                break
        return location

    def list_of_moves(self, move_from, player):
        """returns a list of valid moves for the piece chosen by a player"""
        index = self.get_location(move_from)
        column = index[1]
        row = index[0]

        if self._board[row][column] in self._white_pieces:
            if player == "white":
                list_1 = self._white_pieces
                capture_pieces = self._black_pieces
            else:
                return []

        elif self._board[row][column] in self._black_pieces:
            if player == "black":
                list_1 = self._black_pieces
                capture_pieces = self._white_pieces
            else:
                return []

        if self._board[row][column] == "p" or self._board[row][column] == "P":
            return self.pawn_moves(column, row, player)

        elif self._board[row][column] == "n" or self._board[row][column] == "N":
            return self.knight_moves(column, row, list_1, capture_pieces)

        elif self._board[row][column] == "r" or self._board[row][column] == "R":
            return self.rook_moves(column, row, list_1, capture_pieces)

        elif self._board[row][column] == "b" or self._board[row][column] == "B":
            return self.bishop_moves(column, row, list_1, capture_pieces)

        elif self._board[row][column] == "q" or self._board[row][column] == "Q":
            return self.queen_moves(column, row, list_1, capture_pieces)

        elif self._board[row][column] == "k" or self._board[row][column] == "K":
            return self.king_moves(column, row)
        else:
            return []

    def pawn_moves(self, column, row, player):
        """returns a list of valid moves for a pawn piece"""
        pawn_list = []
        if player == "black":
            if row == 2:
                if self._board[row + 2][column] == ".":
                    pawn_list.append([row + 2, column])
            if self._board[row + 1][column] == ".":
                pawn_list.append([row + 1, column])

            if self._board[row + 1][column + 1] in self._white_pieces:
                pawn_list.append([(row + 1), (column + 1)])

            if self._board[row + 1][column - 1] in self._white_pieces:
                pawn_list.append([(row + 1), (column - 1)])

            return pawn_list

        else:
            if row == 7:
                if self._board[row - 2][column] == ".":
                    pawn_list.append([row - 2, column])
            if self._board[row - 1][column] == ".":
                pawn_list.append([row - 1, column])

            if self._board[row - 1][column - 1] in self._black_pieces:
                pawn_list.append([(row - 1), (column - 1)])
            if self._board[row - 1][column + 1] in self._black_pieces:
                pawn_list.append([(row - 1), (column + 1)])
            return pawn_list

    def rook_moves(self, column, row, list_1, capture_pieces):
        """assigns appropriate variables to the rook helper function and returns a list of valid moves"""
        rook_list = []

        rook_helper(self._board, column + 1, row, 0, 1, capture_pieces, list_1, rook_list)

        rook_helper(self._board, column - 1, row, 0, -1, capture_pieces, list_1, rook_list)

        rook_helper(self._board, column, row + 1, 1, 0, capture_pieces, list_1, rook_list)

        rook_helper(self._board, column, row - 1, -1, 0, capture_pieces, list_1, rook_list)

        return rook_list

    def knight_moves(self, column, row, list_1, capture_pieces):
        """assigns appropriate variables to the knight helper function and returns a list of valid moves"""
        knight_list = []

        values = [-1, 1]

        for value in values:
            knight_helper(self._board, column + 2, row + value, knight_list, capture_pieces, list_1)
            knight_helper(self._board, column - 2, row + value, knight_list, capture_pieces, list_1)
            knight_helper(self._board, column + value, row - 2, knight_list, capture_pieces, list_1)
            knight_helper(self._board, column + value, row + 2, knight_list, capture_pieces, list_1)

        return knight_list

    def bishop_moves(self, column, row, list_1, capture_pieces):
        """assigns appropriate variables to the bishop helper function and returns a list of valid moves"""
        bishop_list = []

        bishop_helper(self._board, column + 1, row - 1, 1, -1, capture_pieces, list_1, bishop_list)

        bishop_helper(self._board, column + 1, row + 1, 1, 1, capture_pieces, list_1, bishop_list)

        bishop_helper(self._board, column - 1, row + 1, -1, 1, capture_pieces, list_1, bishop_list)

        bishop_helper(self._board, column - 1, row - 1, -1, -1, capture_pieces, list_1, bishop_list)
        return bishop_list

    def queen_moves(self, column, row, list_1, capture_pieces):
        """returns a list of valid moves for a players Queen piece by calling the rook and bishop functions"""

        vertical_horizontal_moves = self.rook_moves(column, row, list_1, capture_pieces)
        diagonal_moves = self.bishop_moves(column, row, list_1, capture_pieces)
        queen_list = vertical_horizontal_moves + diagonal_moves
        return queen_list

    def king_moves(self, column, row):
        """assigns appropriate variables to the king helper function and returns a list of valid moves"""

        king_list = []
        row_value = [- 1, 1]

        for value in row_value:
            king_helper(self._board, column + 1, row + value, king_list)
            king_helper(self._board, column - 1, row + value, king_list)
            king_helper(self._board, column, row + value, king_list)
            king_helper(self._board, column + value, row, king_list)

        return king_list


