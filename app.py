# import chess
# import chess.engine
# import chess.pgn

# engine = chess.engine.SimpleEngine.popen_uci("D:\stockfish\stockfish-windows-x86-64-avx2.exe")

# board = chess.Board()
# print(board)
# result = engine.analyse(board, chess.engine.Limit(depth=10))

# print(result)

# engine.quit()



# print("Hello, World!")
# from flask import Flask, render_template, request
# import os

# app = Flask(__name__)

# UPLOAD_FOLDER = "uploads"
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# @app.route("/")
# def home():
#     return render_template("index.html")


# @app.route("/upload", methods=["POST"])
# def upload():
#     file = request.files["file"]

#     if file.filename == "":
#         return "No file selected"

#     filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
#     file.save(filepath)

#     return f"File uploaded: {file.filename}"


# if __name__ == "__main__":
#     app.run(debug=True)
print("Hello, World!")

