from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from Gameboard import Gameboard
import db
# import os, sys
import logging

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = None

'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    move = db.get_move()
    if move is not None:
        db.clear()
    global game
    game = Gameboard()
    return render_template(
        'player1_connect.html', status="Pick a Color."
    )


'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    move = db.get_move()
    global game
    if game is None:
        if move is not None:
            # existing state
            current_turn = move[0]
            board = json.loads(move[1])
            winner = move[2]
            player1 = move[3]
            player2 = move[4]
            remaining_moves = move[5]
            game = Gameboard(
                player1, player2, board, current_turn,
                remaining_moves, winner
            )
        else:
            # empty state with no existing game
            return redirect(url_for('player1_connect'))
    else:
        # empty state with an existing game
        p1_color = request.args.get('color')
        if game.player1 == '' and p1_color is not None:
            game.set_player1_color(p1_color)

    if game.player1 == '' or game.game_result != '':
        return redirect(url_for('player1_connect'))

    return render_template(
        'player1_connect.html', status=game.player1
    )


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    if game is None or game.player1 == '':
        return "Error: Player 1 did not pick color first."

    if game.game_result != '':
        return redirect(url_for('player1_connect'))

    if game.player2 == '':

        if game.player1 == 'red':
            p2_color = 'yellow'
        elif game.player1 == 'yellow':
            p2_color = 'red'
        else:
            return "Error: Player 1 picked an invalid color."

        game.set_player2_color(p2_color)

        db.init_db()
        add_move_to_db()

    return render_template(
        'p2Join.html', status=game.player2
    )


'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
'''


@app.route('/move1', methods=['POST'])
def p1_move():
    column = request.get_json()['column']
    col_num = int(column[-1])
    invalid, reason = game.move_is_invalid('p1', col_num)

    if invalid is False:
        game.perform_move('p1', col_num)
        add_move_to_db()

    result = {
        'move': game.board,
        'invalid': invalid,
        'winner': game.game_result
    }

    if game.game_result != '':
        db.clear()

    if invalid is True:
        result['reason'] = reason

    return result


'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    column = request.get_json()['column']
    col_num = int(column[-1])
    invalid, reason = game.move_is_invalid('p2', col_num)

    if invalid is False:
        game.perform_move('p2', col_num)
        add_move_to_db()

    result = {
        'move': game.board,
        'invalid': invalid,
        'winner': game.game_result
    }

    if game.game_result != '':
        db.clear()

    if invalid is True:
        result['reason'] = reason

    return result


'''
Add move data to database
'''


def add_move_to_db():
    current_turn = game.current_turn
    board = json.dumps(game.board)
    winner = game.game_result
    player1 = game.player1
    player2 = game.player2
    remaining_moves = game.remaining_moves
    new_move = (
        current_turn, board, winner, player1,
        player2, remaining_moves
    )
    db.add_move(new_move)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
