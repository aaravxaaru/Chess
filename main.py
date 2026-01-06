from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [
    ["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"]
]

turn = "white"

@app.route("/")
def index():
    return render_template("index.html", board=board, turn=turn)

@app.route("/move", methods=["POST"])
def move():
    global turn
    data = request.json
    sx, sy, ex, ey = data["sx"], data["sy"], data["ex"], data["ey"]

    piece = board[sx][sy]

    if piece == " ":
        return jsonify(success=False)

    if turn == "white" and piece.islower():
        return jsonify(success=False)

    if turn == "black" and piece.isupper():
        return jsonify(success=False)

    board[ex][ey] = piece
    board[sx][sy] = " "
    turn = "black" if turn == "white" else "white"

    return jsonify(success=True, board=board, turn=turn)

if __name__ == "__main__":
    app.run(debug=True)
