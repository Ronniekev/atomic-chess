# Author: Kevin Penate
# GitHub username: Ronniekev
# Date: 6/4/2024
# Description: Builds an atomic chess game board, that allows two players to move pieces and will return the winner
# of the game. Has helper functions that calculate the moves a piece can make and returns a list of valid moves.


def is_move_valid(move_to, move_list):
    """Check if a move is valid."""
    return move_to in move_list

def bishop_helper(board, col, row, d_col, d_row, capturable, friendly, moves):
    """Compute bishop moves in one direction."""
    for _ in range(8):
        col += d_col
        row += d_row
        if 0 < col < 9 and 0 < row < 9:
            piece = board[row][col]
            if piece in friendly:
                break
            moves.append([row, col])
            if piece in capturable:
                break
        else:
            break


def knight_helper(board, col, row, capturable, friendly, moves):
    """Compute all knight moves."""
    deltas = [(2, 1), (1, 2), (-1, 2), (-2, 1),
              (-2, -1), (-1, -2), (1, -2), (2, -1)]
    for dc, dr in deltas:
        new_col, new_row = col + dc, row + dr
        if 0 < new_col < 9 and 0 < new_row < 9:
            piece = board[new_row][new_col]
            if piece not in friendly:
                moves.append([new_row, new_col])


def rook_helper(board, col, row, d_col, d_row, capturable, friendly, moves):
    """Compute rook moves in one direction."""
    for _ in range(8):
        col += d_col
        row += d_row
        if 0 < col < 9 and 0 < row < 9:
            piece = board[row][col]
            if piece in friendly:
                break
            moves.append([row, col])
            if piece in capturable:
                break
        else:
            break


def king_helper(board, col, row, moves):
    """Compute adjacent king moves."""
    for dc in [-1, 0, 1]:
        for dr in [-1, 0, 1]:
            if dc == 0 and dr == 0:
                continue
            new_col, new_row = col + dc, row + dr
            if 0 < new_col < 9 and 0 < new_row < 9 and board[new_row][new_col] == ".":
                moves.append([new_row, new_col])


def king_check_help(board, col, row, king_check):
    """Collect chess pieces to near explosion."""
    if 0 < col < 9 and 0 < row < 9:
        king_check.append(board[row][col])
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
        if self.get_game_state() != "UNFINISHED":
            return False

        player = self.player_turn()
        valid_moves = self.list_of_moves(move_from, player)
        source = self.get_location(move_from)
        destination = self.get_location(move_to)

        
        if is_move_valid(destination, valid_moves):
            if self._board[destination[0]][destination[1]] == ".":
                self._board[destination[0]][destination[1]] = self._board[source[0]][source[1]]
                self._board[source[0]][source[1]] = "."
                self._player_turn += 1
                return True
            elif not self.explosion(destination):
                return False
            else:
                self.explosion(destination)
                self._board[source[0]][source[1]] = "."
                self._board[destination[0]][destination[1]] = "."
                self._player_turn += 1
                return True
        return False

    def get_game_state(self):
        """Computs game status."""

        if "k" in self._white_pieces and "K" in self._black_pieces:
            return "UNFINISHED"
        elif "k" in self._white_pieces:
            return "WHITE_WON"
        else:
            return "BLACK_WON"

    def explosion(self, move):
        """Computes pieces valid to be removed during an explosion."""
        row, col = move
        check = []
        for dc, dr in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]:
            king_check_help(self._board, col+dc, row+dr, check)

        if "K" in check and "k" in check:
            return False

        for dc, dr in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]:
            row, col = row+dr, col+dc
            if 0 < col < 9 and 0 < row < 9:
                if self._board[row][col] not in ("p", "P"):
                    self.remove_king(col, row)
        return True

    def remove_king(self, col, row):
        """Computes King to be removed."""
        piece = self._board[row][col]
        if piece == "k":
            if "k" in self._white_pieces:
                self._white_pieces.remove('k')  

        elif piece == "K":
            if "K" in self._black_pieces:
                self._black_pieces.remove('K')
        
        self._board[row][col] = "."
        self.get_game_state()
        return

    def print_board(self):
        """Prints current board placement"""
        for row in self._board:
            print(*row)

    def player_turn(self):
        """Computes who's turn it is"""

        if self._player_turn % 2 == 0:
            return "white"
        else:
            return "black"

    def get_location(self, move):
        """returns int variable for index location of pieces, if the location is not on the board it will return
        False"""
        rank_map = {"8": 1, "7": 2, "6": 3, "5": 4, "4": 5, "3": 6, "2": 7, "1": 8}
        file = move[0]
        rank = move[1]
        if rank not in rank_map or file not in self._board[0]:
            return []
        return [rank_map[rank], self._board[0].index(file)]

    def list_of_moves(self, move_from, player):
        """returns a list of valid moves for the piece chosen by a player"""
        index = self.get_location(move_from)
        if not index:
            return []
        row, col= index
        piece = self._board[row][col]

        friendly, capturable = (
            (self._white_pieces, self._black_pieces) if player == "white" else
            (self._black_pieces, self._white_pieces)
        )

        if piece not in friendly:
            return []

        piece_type = piece.lower()
        dispatch = {
            "p": self.pawn_moves,
            "n": lambda c, r: self.knight_moves(col, row, friendly, capturable),
            "r": lambda c, r: self.rook_moves(col, row, friendly, capturable),
            "b": lambda c, r: self.bishop_moves(col, row, friendly, capturable),
            "q": lambda c, r: self.queen_moves(col, row, friendly, capturable),
            "k": lambda c, r: self.king_moves(col, row),
        }

        return dispatch[piece_type](col, row)
        

    def pawn_moves(self, col, row):
        """returns a list of valid moves for a pawn piece"""
        moves = []
        direction = 1 if self.player_turn() == "black" else -1
        start_row = 2 if direction == 1 else 7
        capturables = self._white_pieces if direction == 1 else self._black_pieces

        if self._board[row + direction][col] == ".":
            moves.append([row + direction, col])
            if row == start_row and self._board[row + 2 * direction][col] == ".":
                moves.append([row + 2 * direction, col])

        for dc in [-1, 1]:
            if 0 < col + dc < 9 and self._board[row + direction][col + dc] in capturables:
                moves.append([row + direction, col + dc])

        return moves

    def rook_moves(self, col, row, friendly, capturable):
        """Computes valid Rook Moves."""
        moves = []
        for dc, dr in [(1,0), (-1,0), (0,1), (0,-1)]:

            rook_helper(self._board, col, row, dc, dr, capturable, friendly, moves)
        return moves

    def knight_moves(self, col, row, friendly, capturable):
        """Computes knight moves."""
        moves = []
        knight_helper(self._board, col, row, capturable, friendly, moves)
        return capturable

    def bishop_moves(self, col, row, friendly, capturable):
        """Computes bishop valid moves."""
        bishop_list = []
        for dc, dr in [(1,1), (1,-1), (-1,1), (-1,-1)]:
            bishop_helper(self._board, col, row, dc, dr, capturable, friendly, bishop_list)
        return bishop_list

    def queen_moves(self, col, row, friendly, capturable):
        """Computes Queens valid move."""

        vertical_horizontal_moves = self.rook_moves(col, row, friendly, capturable)
        diagonal_moves = self.bishop_moves(col, row, friendly, capturable)
        queen_list = vertical_horizontal_moves + diagonal_moves
        return queen_list

    def king_moves(self, col, row):
        """aComputes King Moves"""
        moves = []
        king_helper(self._board, col, row, moves)

        return moves


