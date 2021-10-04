import unittest
import unittest.mock
import io
import json
import sqlite3
from sqlite3 import Error
import db


def execute_sql_query(query):
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.execute(query)
        return cur.fetchone()
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


class Test_TestDb(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_init_db(self, mock_stdout):
        # checks if table creation is successful
        table_name = 'GAME'
        query = f"DROP TABLE IF EXISTS {table_name}"
        execute_sql_query(query)

        db.init_db()

        query = "SELECT name FROM sqlite_master WHERE type='table' " \
                + f"AND name='{table_name}';"
        res = execute_sql_query(query)

        self.assertEqual(res[0], 'GAME')

        expected_output = 'Database Online, table created\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_init_db_if_table_already_exists(self, mock_stdout):
        # checks table creation error if table already exists
        table_name = 'GAME'
        query = f"DROP TABLE IF EXISTS {table_name}"
        execute_sql_query(query)

        db.init_db()
        db.init_db()

        expected_output = 'Database Online, table created\n' + \
            'table GAME already exists\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_add_move(self, mock_stdout):
        # checks if move info insersion is successful
        table_name = 'GAME'
        query = f"DROP TABLE IF EXISTS {table_name}"
        execute_sql_query(query)

        db.init_db()

        current_turn = 'p1'
        board = [[0 for x in range(7)] for y in range(6)]
        winner = ''
        player1 = 'red'
        player2 = 'yellow'
        remaining_moves = 42
        new_move = (
            current_turn, json.dumps(board), winner, player1,
            player2, remaining_moves
        )
        db.add_move(new_move)

        query = "SELECT * FROM GAME WHERE " \
                + f"current_turn='{current_turn}' AND board='{board}' AND " \
                + f"winner='{winner}' AND player1='{player1}' AND " \
                + f"player2='{player2}' AND remaining_moves={remaining_moves};"
        res = execute_sql_query(query)

        self.assertIsNotNone(res)

        expected_output = 'Database Online, table created\n' + \
            'Database Online, move added\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_add_move_if_table_not_created(self, mock_stdout):
        # checks move info insersion error if table not created
        table_name = 'GAME'
        query = f"DROP TABLE IF EXISTS {table_name}"
        execute_sql_query(query)

        current_turn = 'p1'
        board = [[0 for x in range(7)] for y in range(6)]
        winner = ''
        player1 = 'red'
        player2 = 'yellow'
        remaining_moves = 42
        new_move = (
            current_turn, json.dumps(board), winner, player1,
            player2, remaining_moves
        )
        db.add_move(new_move)

        expected_output = 'no such table: GAME\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_get_move(self, mock_stdout):
        # checks if move fetching is successful and correct
        table_name = 'GAME'
        query = f"DROP TABLE IF EXISTS {table_name}"
        execute_sql_query(query)

        db.init_db()

        current_turn = 'p1'
        board = [[0 for x in range(7)] for y in range(6)]
        winner = ''
        player1 = 'red'
        player2 = 'yellow'
        remaining_moves = 42
        move1 = (
            current_turn, json.dumps(board), winner, player1,
            player2, remaining_moves
        )
        db.add_move(move1)

        board[len(board) - 1][0] = 'red'
        remaining_moves -= 1
        current_turn = 'p2'
        move2 = (
            current_turn, json.dumps(board), winner, player1,
            player2, remaining_moves
        )
        db.add_move(move2)

        res_move = db.get_move()
        self.assertIsNotNone(res_move)
        res_remaining_moves = res_move[5]

        self.assertEqual(res_remaining_moves, remaining_moves)

        expected_output = 'Database Online, table created\n' + \
            'Database Online, move added\n' + \
            'Database Online, move added\n' + \
            'Database Online, move fetched\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_get_move_if_empty_state(self, mock_stdout):
        # checks move fetching error if empty state
        table_name = 'GAME'
        query = f"DROP TABLE IF EXISTS {table_name}"
        execute_sql_query(query)

        db.init_db()

        res_move = db.get_move()
        self.assertIsNone(res_move)

        expected_output = 'Database Online, table created\n' + \
            'Database Online, move fetched\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_get_move_if_table_not_created(self, mock_stdout):
        # checks move fetching error if table not created
        table_name = 'GAME'
        query = f"DROP TABLE IF EXISTS {table_name}"
        execute_sql_query(query)

        res_move = db.get_move()
        self.assertIsNone(res_move)

        expected_output = 'no such table: GAME\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_clear(self, mock_stdout):
        # checks if table deletion is successful
        table_name = 'GAME'
        query = f"DROP TABLE IF EXISTS {table_name}"
        execute_sql_query(query)

        db.init_db()

        db.clear()

        query = "SELECT name FROM sqlite_master WHERE type='table' " \
                + f"AND name='{table_name}';"
        res = execute_sql_query(query)

        self.assertIsNone(res)

        expected_output = 'Database Online, table created\n' + \
            'Database Cleared\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_clear_if_table_not_created(self, mock_stdout):
        # checks table deletion error if table not created
        table_name = 'GAME'
        query = f"DROP TABLE IF EXISTS {table_name}"
        execute_sql_query(query)

        db.clear()

        expected_output = 'no such table: GAME\n'
        self.assertEqual(mock_stdout.getvalue(), expected_output)
