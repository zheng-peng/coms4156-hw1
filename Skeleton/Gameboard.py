# import db

class Gameboard():
    def __init__(
        self, player1="", player2="",
        board=None,
        current_turn="p1", remaining_moves=42,
        game_result=""
    ):
        self.player1 = player1
        self.player2 = player2
        if board is not None:
            self.board = board
        else:
            self.board = [[0 for x in range(7)] for y in range(6)]
        self.current_turn = current_turn
        self.remaining_moves = remaining_moves
        self.game_result = game_result

    def set_player1_color(self, color):
        self.player1 = color

    def set_player2_color(self, color):
        self.player2 = color

    def move_is_invalid(self, player, col):
        if self.player1 == '':
            return True, 'Please pick a color first.'
        if self.player2 == '':
            return True, 'Please wait for player 2 to join.'
        if self.game_result != '':
            return True, 'Please start a new game.'
        if self.current_turn != player:
            return True, 'Please wait for your turn.'
        if self.remaining_moves <= 0:
            return True, 'The game board is full.'
        if self.board[0][col - 1] != 0:
            return True, 'The picked column is full.'
        return False, ''

    def perform_move(self, player, col):
        if player == 'p1':
            color = self.player1
        else:
            color = self.player2

        board = self.board
        row = len(board)
        while row >= 1 and board[row - 1][col - 1] != 0:
            row -= 1

        if row >= 1:
            board[row - 1][col - 1] = color
            self.remaining_moves -= 1

            if player == 'p1':
                self.current_turn = 'p2'
            else:
                self.current_turn = 'p1'

            # after at least 7 steps, check if there is a winner
            if self.remaining_moves <= 35:
                self.update_winner(player, row, col)

    def update_winner(self, player, row, col):
        if player == 'p1':
            color = self.player1
        else:
            color = self.player2

        win_h = self.check_winner_horizontal(color, row, col)
        win_v = self.check_winner_vertical(color, row, col)
        win_d = self.check_winner_diagnal(color, row, col)
        win = win_h or win_v or win_d

        if win is True:
            if player == 'p1':
                self.game_result = "Player 1"
            else:
                self.game_result = "Player 2"

    def check_winner_horizontal(self, color, row, col):
        board = self.board
        left = col - 3 if col - 3 >= 1 else 1
        right = col + 3 if col + 3 <= len(board[0]) else len(board[0])
        cur_col = left
        connect = 0

        while left <= cur_col and cur_col <= right:
            if board[row - 1][cur_col - 1] == color:
                connect += 1
                if connect >= 4:
                    return True
            else:
                connect = 0
            cur_col += 1

        return False

    def check_winner_vertical(self, color, row, col):
        board = self.board
        up = row - 3 if row - 3 >= 1 else 1
        down = row + 3 if row + 3 <= len(board) else len(board)
        cur_row = up
        connect = 0

        while up <= cur_row and cur_row <= down:
            if board[cur_row - 1][col - 1] == color:
                connect += 1
                if connect >= 4:
                    return True
            else:
                connect = 0
            cur_row += 1

        return False

    def check_winner_diagnal(self, color, row, col):
        board = self.board
        up = row - 3
        down = row + 3
        left = col - 3
        right = col + 3
        # check upper-left to lower-right
        cur_row = up
        cur_col = left
        connect = 0
        while (
            up <= cur_row and cur_row <= down and
            left <= cur_col and cur_col <= right
        ):
            if (
                1 <= cur_row and cur_row <= len(board) and
                1 <= cur_col and cur_col <= len(board[0]) and
                board[cur_row - 1][cur_col - 1] == color
            ):
                connect += 1
                if connect >= 4:
                    return True
            else:
                connect = 0
            cur_row += 1
            cur_col += 1

        # check lower-left to upper-right
        cur_row = down
        cur_col = left
        connect = 0
        while (
            up <= cur_row and cur_row <= down and
            left <= cur_col and cur_col <= right
        ):
            if (
                1 <= cur_row and cur_row <= len(board) and
                1 <= cur_col and cur_col <= len(board[0]) and
                board[cur_row - 1][cur_col - 1] == color
            ):
                connect += 1
                if connect >= 4:
                    return True
            else:
                connect = 0
            cur_row -= 1
            cur_col += 1

        return False
