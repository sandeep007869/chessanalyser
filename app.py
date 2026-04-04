print("Hello, World!")

from flask import Flask, render_template, request
import os
import chess.pgn
import chess,chess.engine 
engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish.exe")
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")
from flask import request, redirect, url_for
import io

uploaded_moves = []

import chess.engine

@app.route("/upload", methods=["POST"])
def upload():
    global uploaded_moves

    engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish.exe")

    file = request.files['file']
    pgn_text = file.read().decode("utf-8")

    pgn = io.StringIO(pgn_text)
    game = chess.pgn.read_game(pgn)

    board = game.board()
    uploaded_moves = []

    for move in game.mainline_moves():
        info_before = engine.analyse(board, chess.engine.Limit(time=0.05))
        score_before = info_before["score"].white().score(mate_score=10000)

        san = board.san(move)
        board.push(move)

        info_after = engine.analyse(board, chess.engine.Limit(time=0.05))
        score_after = info_after["score"].white().score(mate_score=10000)

        diff = (score_after - score_before) if score_before and score_after else 0

        # classification
        if diff >= 0:
            tag = "best"
        elif diff >= -50:
            tag = "good"
        elif diff >= -100:
            tag = "inaccuracy"
        elif diff >= -300:
            tag = "mistake"
        else:
            tag = "blunder"

        uploaded_moves.append({
            "move": san,
            "fen": board.fen(),
            "eval": score_after,
            "diff": diff,
            "tag": tag
        })

    engine.quit()  

    return redirect(url_for("board"))


@app.route("/board")
def board():
    return render_template("board.html")

from flask import jsonify

@app.route("/analysis")
def analysis():
    return jsonify(uploaded_moves)

engine.quit()
if __name__ == "__main__":
    app.run(debug=True)
