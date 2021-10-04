import sqlite3
from sqlite3 import Error

'''
Initializes the Table GAME
Do not modify
'''


def init_db():
    # creates Table
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute('CREATE TABLE GAME(current_turn TEXT, board TEXT,' +
                     'winner TEXT, player1 TEXT, player2 TEXT' +
                     ', remaining_moves INT)')
        print('Database Online, table created')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
move is a tuple (current_turn, board, winner, player1, player2,
remaining_moves)
Insert Tuple into table
'''


def add_move(move):  # will take in a tuple
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        current_turn = move[0]
        board = move[1]
        winner = move[2]
        player1 = move[3]
        player2 = move[4]
        remaining_moves = move[5]
        conn.execute(
            'INSERT INTO GAME '
            'VALUES (?,?,?,?,?,?);',
            (
                current_turn, board, winner,
                player1, player2, remaining_moves
            )
        )
        conn.commit()
        print('Database Online, move added')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


'''
Get the last move played
return (current_turn, board, winner, player1, player2, remaining_moves)
'''


def get_move():
    # will return tuple(current_turn, board, winner, player1, player2,
    # remaining_moves) or None if db fails
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        cur = conn.execute(
            'SELECT * FROM GAME '
            'ORDER BY remaining_moves limit 1;'
        )
        row = cur.fetchone()
        print('Database Online, move fetched')
        return row
    except Error as e:
        print(e)
        return None

    finally:
        if conn:
            conn.close()


'''
Clears the Table GAME
Do not modify
'''


def clear():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db')
        conn.execute("DROP TABLE GAME")
        print('Database Cleared')
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()
