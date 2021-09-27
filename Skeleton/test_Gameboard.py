import unittest
from Gameboard import Gameboard


def play_game(p1_color=None, p2_color=None, moves=None):
    '''
    simulate player moves
    p1_color: str, p2_color: str, moves: [['p1' or 'p2', col_num(1-based)],...]
    '''
    game = Gameboard()
    if p1_color is not None:
        game.set_player1_color(p1_color)
    if p2_color is not None:
        game.set_player2_color(p2_color)
    if moves is not None:
        for move in moves:
            player = move[0]
            col = move[1]
            invalid, reason = game.move_is_invalid(player, col)
            if invalid is True:
                continue
            game.perform_move(player, col)
    return game


class Test_TestGameboard(unittest.TestCase):

    def test_init(self):
        # Checks if the game is properly initialized
        game = play_game()
        self.assertIsInstance(game, Gameboard)

    def test_set_player1_color(self):
        # Checks if player 1 color is properly set
        game = play_game('red')
        self.assertEqual(game.player1, 'red')

    def test_set_player2_color(self):
        # Checks if player 2 color is properly set
        game = play_game(None, 'yellow')
        self.assertEqual(game.player2, 'yellow')

    def test_move_is_invalid_if_player_1_no_color(self):
        # Checks if correct message is returned if player 1 has not picked a
        # color
        game = play_game()
        self.assertEqual(
            game.move_is_invalid('p1', 1),
            (True, 'Please pick a color first.')
        )

    def test_move_is_invalid_if_player_2_no_color(self):
        # Checks if correct message is returned if player 2 has not joined
        game = play_game('red')
        self.assertEqual(
            game.move_is_invalid('p1', 1),
            (True, 'Please wait for player 2 to join.')
        )

    def test_move_is_invalid_if_winner_exists(self):
        # Checks if correct message is returned if a winner exists
        '''
        resulting board visualized:
        ---------------
        | | | | | | | |
        | | | | | | | |
        |r| | | | | | |
        |r|y| | | | | |
        |r|y| | | | | |
        |r|y| | | | | |
        ---------------
        '''
        moves = [
            ['p1', 1], ['p2', 2], ['p1', 1], ['p2', 2],
            ['p1', 1], ['p2', 2], ['p1', 1]
        ]
        game = play_game('red', 'yellow', moves)
        self.assertEqual(
            game.move_is_invalid('p1', 1),
            (True, 'Please start a new game.')
        )

    def test_move_is_invalid_if_not_current_turn(self):
        # Checks if correct message is returned if the current turn does not
        # match
        game = play_game('red', 'yellow')
        self.assertEqual(
            game.move_is_invalid('p2', 1),
            (True, 'Please wait for your turn.')
        )

    def test_move_is_invalid_if_no_remaining_moves(self):
        # Checks if correct message is returned if the board is full
        '''
        resulting board visualized:
        ---------------
        |r|y|r|y|r|y|y|
        |r|y|r|y|r|y|r|
        |y|r|y|r|y|r|y|
        |y|r|y|r|y|r|y|
        |r|y|r|y|r|y|r|
        |r|y|r|y|r|y|r|
        ---------------
        '''
        moves = [
            ['p1', 1], ['p2', 2], ['p1', 1], ['p2', 2],
            ['p1', 3], ['p2', 4], ['p1', 3], ['p2', 4],
            ['p1', 5], ['p2', 6], ['p1', 5], ['p2', 6],
            ['p1', 7], ['p2', 1], ['p1', 7], ['p2', 1],
            ['p1', 2], ['p2', 3], ['p1', 2], ['p2', 3],
            ['p1', 4], ['p2', 5], ['p1', 4], ['p2', 5],
            ['p1', 6], ['p2', 7], ['p1', 6], ['p2', 7],
            ['p1', 1], ['p2', 2], ['p1', 1], ['p2', 2],
            ['p1', 3], ['p2', 4], ['p1', 3], ['p2', 4],
            ['p1', 5], ['p2', 6], ['p1', 5], ['p2', 6],
            ['p1', 7], ['p2', 7]
        ]
        game = play_game('red', 'yellow', moves)
        self.assertEqual(
            game.move_is_invalid('p1', 1),
            (True, 'The game board is full.')
        )

    def test_move_is_invalid_if_picked_column_full(self):
        # Checks if correct message is returned if the picked column is full
        '''
        resulting board visualized:
        ---------------
        |y| | | | | | |
        |r| | | | | | |
        |y| | | | | | |
        |r| | | | | | |
        |y| | | | | | |
        |r| | | | | | |
        ---------------
        '''
        moves = [
            ['p1', 1], ['p2', 1], ['p1', 1], ['p2', 1],
            ['p1', 1], ['p2', 1]
        ]
        game = play_game('red', 'yellow', moves)
        self.assertEqual(
            game.move_is_invalid('p1', 1),
            (True, 'The picked column is full.')
        )

    def test_perform_move_result_board_state(self):
        # Checks if the board is correctly updated after performing a move
        '''
        resulting board visualized:
        ---------------
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        |r| | | | | | |
        ---------------
        '''
        moves = [
            ['p1', 1]
        ]
        game = play_game('red', 'yellow', moves)
        self.assertEqual(game.board[5][0], 'red')

    def test_perform_move_result_remaining_moves(self):
        # Checks if the number of remaining moves is correctly updated after
        # performing a move
        '''
        resulting board visualized:
        ---------------
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        |r| | | | | | |
        ---------------
        '''
        moves = [
            ['p1', 1]
        ]
        game = play_game('red', 'yellow', moves)
        self.assertEqual(game.remaining_moves, 41)

    def test_perform_move_result_current_turn(self):
        # Checks if the current turn is correctly updated after performing
        # a move
        '''
        resulting board visualized:
        ---------------
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        |r| | | | | | |
        ---------------
        '''
        moves = [
            ['p1', 1]
        ]
        game = play_game('red', 'yellow', moves)
        self.assertEqual(game.current_turn, 'p2')

    def test_update_winner_player1(self):
        # Checks if there is a winning move for player 1
        '''
        resulting board visualized:
        ---------------
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        |y|y|y| | | | |
        |r|r|r|r| | | |
        ---------------
        '''
        moves = [
            ['p1', 1], ['p2', 1], ['p1', 2], ['p2', 2],
            ['p1', 3], ['p2', 3]
        ]
        game = play_game('red', 'yellow', moves)
        game.board[5][3] = 'red'
        game.update_winner('p1', 6, 4)
        self.assertEqual(game.winner, 'Player 1')

    def test_update_winner_player2(self):
        # Checks if there is a winning move for player 2
        '''
        resulting board visualized:
        ---------------
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        |y|y|y|y|r| | |
        |r|r|r|y|r| | |
        ---------------
        '''
        moves = [
            ['p1', 1], ['p2', 1], ['p1', 2], ['p2', 2],
            ['p1', 3], ['p2', 3], ['p1', 5], ['p2', 4],
            ['p1', 5]
        ]
        game = play_game('red', 'yellow', moves)
        game.board[4][3] = 'yellow'
        game.update_winner('p2', 5, 4)
        self.assertEqual(game.winner, 'Player 2')

    def test_check_winner_horizontal(self):
        # Checks if there is a winning move in horizontal direction
        '''
        resulting board visualized:
        ---------------
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        |y|y|y| | | | |
        |r|r|r|r| | | |
        ---------------
        '''
        moves = [
            ['p1', 1], ['p2', 1], ['p1', 2], ['p2', 2],
            ['p1', 3], ['p2', 3]
        ]
        game = play_game('red', 'yellow', moves)
        game.board[5][3] = 'red'
        self.assertTrue(game.check_winner_horizontal('red', 6, 4))

    def test_check_winner_vertical(self):
        # Checks if there is a winning move in vertical direction
        '''
        resulting board visualized:
        ---------------
        | | | | | | | |
        |y| | | | | | |
        |y| | | | | | |
        |y| | | | | | |
        |y| | | | | | |
        |r| |r|r|r| | |
        ---------------
        '''
        moves = [
            ['p1', 1], ['p2', 1], ['p1', 3], ['p2', 1],
            ['p1', 4], ['p2', 1], ['p1', 5]
        ]
        game = play_game('red', 'yellow', moves)
        game.board[1][0] = 'yellow'
        self.assertTrue(game.check_winner_vertical('yellow', 2, 1))

    def test_check_winner_diagnal_upper_left_to_lower_right(self):
        # Checks if there is a winning move in diagnal direction
        # (upper-left to lower-right)
        '''
        resulting board visualized:
        ---------------
        | | | | | | | |
        | | | | | | | |
        |r| | |y| | | |
        |y|r| |y| | | |
        |y|y|r|r| | | |
        |r|r|y|r| | | |
        ---------------
        '''
        moves = [
            ['p1', 1], ['p2', 1], ['p1', 2], ['p2', 2],
            ['p1', 4], ['p2', 3], ['p1', 3], ['p2', 1],
            ['p1', 4], ['p2', 4], ['p1', 2], ['p2', 4],
            ['p1', 1]
        ]
        game = play_game('red', 'yellow', moves)
        self.assertTrue(game.check_winner_diagnal('red', 3, 1))

    def test_check_winner_diagnal_lower_left_to_upper_right(self):
        # Checks if there is a winning move in diagnal direction
        # (lower-left to upper-right)
        '''
        resulting board visualized:
        ---------------
        | | | | | | | |
        | | | | | | | |
        | | | |r| | | |
        | | |r|r| | | |
        | |r|y|y| | | |
        |r|y|y|r|y| | |
        ---------------
        '''
        moves = [
            ['p1', 1], ['p2', 2], ['p1', 2], ['p2', 3],
            ['p1', 4], ['p2', 3], ['p1', 3], ['p2', 4],
            ['p1', 4], ['p2', 5], ['p1', 4]
        ]
        game = play_game('red', 'yellow', moves)
        self.assertTrue(game.check_winner_diagnal('red', 3, 4))
