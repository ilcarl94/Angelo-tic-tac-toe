from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

import copy

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

global global_winner
global move
global boards

def available_moves(game, player):

    available_moves = []
    for i in range(3):
        for j in range(3):
            if not game[i][j]:
                temporary_game = copy.deepcopy(game)
                temporary_game[i][j] = player
                available_moves.append(temporary_game)

    return available_moves


def full_board(game):
    full_board = True

    for i in range(3):
        for j in range(3):
            if not game[i][j]:
                full_board = False

    return full_board

def calculate_score(game):
    if game[0][0] == "X" and game[1][0] == "X" and game[2][0] == "X":
        return 10
    elif game[0][1] == "X" and game[1][1] == "X" and game[2][1] == "X":
        return 10
    elif game[0][2] == "X" and game[1][2] == "X" and game[2][2] == "X":
        return 10
    elif game[0][0] == "X" and game[0][1] == "X" and game[0][2] == "X":
        return 10
    elif game[1][0] == "X" and game[1][1] == "X" and game[1][2] == "X":
        return 10
    elif game[2][0] == "X" and game[2][1] == "X" and game[2][2] == "X":
        return 10
    elif game[0][0] == "X" and game[1][1] == "X" and game[2][2] == "X":
        return 10
    elif game[2][0] == "X" and game[1][1] == "X" and game[0][2] == "X":
        return 10
    elif game[0][0] == "O" and game[1][0] == "O" and game[2][0] == "O":
        return -10
    elif game[0][1] == "O" and game[1][1] == "O" and game[2][1] == "O":
        return -10
    elif game[0][2] == "O" and game[1][2] == "O" and game[2][2] == "O":
        return -10
    elif game[0][0] == "O" and game[0][1] == "O" and game[0][2] == "O":
        return -10
    elif game[1][0] == "O" and game[1][1] == "O" and game[1][2] == "O":
        return -10
    elif game[2][0] == "O" and game[2][1] == "O" and game[2][2] == "O":
        return -10
    elif game[0][0] == "O" and game[1][1] == "O" and game[2][2] == "O":
        return -10
    elif game[2][0] == "O" and game[1][1] == "O" and game[0][2] == "O":
        return -10
    else:
        return 0


def is_winner(turn, row, col):
    if row == 0 and col == 0:
        if session["board"][row + 1][col + 1] == turn and session["board"][row + 2][col + 2] == turn:
            return turn
        elif session["board"][row][col + 1] == turn and session["board"][row][col + 2] == turn:
            return turn
        elif session["board"][row + 1][col] == turn and session["board"][row + 2][col] == turn:
            return turn
    elif row == 0 and col == 1:
        if session["board"][row + 1][col] == turn and session["board"][row + 2][col] == turn:
            return turn
        elif session["board"][row][col - 1] == turn and session["board"][row][col + 1] == turn:
            return turn
    elif row == 0 and col == 2:
        if session["board"][row + 1][col - 1] == turn and session["board"][row + 2][col - 2] == turn:
            return turn
        elif session["board"][row][col - 1] == turn and session["board"][row][col - 2] == turn:
            return turn
        elif session["board"][row + 1][col] == turn and session["board"][row + 2][col] == turn:
            return turn
    elif row == 1 and col == 0:
        if session["board"][row][col + 1] == turn and session["board"][row][col + 2] == turn:
            return turn
        elif session["board"][row - 1][col] == turn and session["board"][row + 1][col] == turn:
            return turn
    elif row == 1 and col == 1:
        if session["board"][row - 1][col + 1] == turn and session["board"][row + 1][col - 1] == turn:
            return turn
        elif session["board"][row - 1][col - 1] == turn and session["board"][row + 1][col + 1] == turn:
            return turn
        elif session["board"][row - 1][col] == turn and session["board"][row + 1][col] == turn:
            return turn
        elif session["board"][row][col - 1] == turn and session["board"][row][col + 1] == turn:
            return turn
    elif row == 1 and col == 2:
        if session["board"][row][col - 1] == turn and session["board"][row][col - 2] == turn:
            return turn
        elif session["board"][row - 1][col] == turn and session["board"][row + 1][col] == turn:
            return turn
    elif row == 2 and col == 0:
        if session["board"][row - 1][col + 1] == turn and session["board"][row - 2][col + 2] == turn:
            return turn
        elif session["board"][row][col + 1] == turn and session["board"][row][col + 2] == turn:
            return turn
        elif session["board"][row - 1][col] == turn and session["board"][row - 2][col] == turn:
            return turn
    elif row == 2 and col == 1:
        if session["board"][row - 1][col] == turn and session["board"][row - 2][col] == turn:
            return turn
        elif session["board"][row][col - 1] == turn and session["board"][row][col + 1] == turn:
            return turn
    elif row == 2 and col == 2:
        if session["board"][row - 1][col - 1] == turn and session["board"][row - 2][col - 2] == turn:
            return turn
        elif session["board"][row][col - 1] == turn and session["board"][row][col - 2] == turn:
            return turn
        elif session["board"][row - 1][col] == turn and session["board"][row - 2][col] == turn:
            return turn
    else:
        return None
    
def minimax(game, player, depth):

    score = calculate_score(game)
    if score == 10 or score == -10:
        return score
    if full_board(game):
        return 0
    else:
        legal_moves = available_moves(game, player)
        if player == "X":
            best_value = -100
            for try_move in legal_moves:
                best_value = max(best_value, minimax(try_move, "O", depth + 1)) - depth

        else:
            best_value = 100
            for try_move in legal_moves:
                best_value = min(best_value, minimax(try_move, "X", depth + 1)) + depth

        return best_value
        


@app.route("/")
def index():

    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"

        global global_winner
        global move
        global boards

        global_winner = None
        move = 0
        boards = []
        boards.append([[None, None, None], [None, None, None], [None, None, None]])


    ending_draw = False

    if full_board(session["board"]) and global_winner is None:
        ending_draw = True

    return render_template("game.html", game=session["board"], turn=session["turn"], winner=global_winner, draw=ending_draw, empty=[[None, None, None], [None, None, None], [None, None, None]])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    global global_winner
    global boards
    global move

    move = move + 1

    if session["turn"] == "X":
        session["board"][row][col] = "X"
        
        if (move > (len(boards) - 1)):
            boards.append(session["board"])
        else:
            boards[move] = session["board"]
        if is_winner(turn=session["turn"], row=row, col=col) == "X":
            global_winner = "X"
        session["turn"] = "O"
    elif session["turn"] == "O":
        session["board"][row][col] = "O"
        if (move > (len(boards) - 1)):
            boards.append(session["board"])
        else:
            boards[move] = session["board"]
        if is_winner(turn=session["turn"], row=row, col=col) == "O":
            global_winner = "O"
        session["turn"] = "X"

    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    global move
    global boards
    global global_winner

    session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    session["turn"] = "X"
    move = 0
    for board in boards:
        board = [[None, None, None], [None, None, None], [None, None, None]]
    global_winner = None
    return redirect(url_for("index"))

@app.route("/undo")
def undo():
    global move
    global boards

    boards[move] = [[None, None, None], [None, None, None], [None, None, None]]
    move = move - 1
    session["board"] = boards[move]
    
    if session["turn"] == "X":
        session["turn"] = "O"
    elif session["turn"] == "O":
        session["turn"] = "X" 

    return redirect(url_for("index"))

@app.route("/computer")
def computer():

    global move
    global global_winner
    global boards

    temporary_board = session["board"]
    temporary_turn = session["turn"]

    if temporary_turn == "X":
        temporary_opposite_turn = "O"
        best_val = -100
    else:
        temporary_opposite_turn = "X"
        best_val = 100

    moves = available_moves(temporary_board, temporary_turn)

    for test_move in moves:
        move_val = minimax(test_move, temporary_opposite_turn, 0)
        if temporary_turn == "X":
            if move_val > best_val:
                best_move = test_move
                best_val = move_val
        else:
            if move_val < best_val:
                best_move = test_move
                best_val = move_val

    move = move + 1

    if temporary_turn == "X":
        session["board"] = best_move
        if (move > (len(boards) - 1)):
            boards.append(session["board"])
        else:
            boards[move] = session["board"]
        if calculate_score(session["board"]) > 0:
            global_winner = "X"
        session["turn"] = "O"
    else:
        session["board"] = best_move
        if (move > (len(boards) - 1)):
            boards.append(session["board"])
        else:
            boards[move] = session["board"]
        if calculate_score(session["board"]) < 0:
            global_winner = "O"
        session["turn"] = "X"

    return redirect(url_for("index"))


