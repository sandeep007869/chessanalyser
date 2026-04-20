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
    return render_template("homepage.html")

@app.route("/index",methods=["POST"])
def index():
    return render_template("index.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")
@app.route("/rules")
def rules():
    return render_template("rules.html")
@app.route("/pgnguide")
def pgnguide():
    return render_template("pgnguide.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/chess.com pgn guide")
def chessp():
    return render_template("chessp.html")
@app.route("/lichess.com pgn guide")
def lichessp():
    return render_template("lichessp.html")


from flask import request, redirect, url_for
import io

uploaded_moves = []

import chess.engine

@app.route("/upload", methods=["POST"])
def upload():
    global uploaded_moves
    engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish.exe")

    file = request.files['file']
    error="please upload a pgn file"
    if not file or not file.filename.endswith('.pgn'):
        return render_template("index.html",error=error)
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
        
        if -50 <= diff <= 50:
            tag = "good"
        elif -100<= diff <= 100:
            tag = "inaccuracy"
        elif -200<= diff<= 200:
            tag = "mistake"
        elif -300<=diff <=300:
            tag = "blunder"
        else:
            tag = "best"

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
