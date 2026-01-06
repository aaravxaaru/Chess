from flask import Flask, request, jsonify, render_template_string

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

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Offline Chess</title>
<style>
body{font-family:Arial;text-align:center;background:#222;color:#fff}
table{margin:auto;border-collapse:collapse}
td{
 width:60px;height:60px;font-size:40px;
 text-align:center;cursor:pointer
}
.w{background:#f0d9b5;color:black}
.b{background:#b58863;color:black}
</style>
</head>
<body>

<h1>♟️ Offline Chess</h1>
<h3 id="turn">White's Turn</h3>

<table id="board"></table>

<script>
let board = {{ board | tojson }};
let turn = "{{ turn }}";
let selected = null;

const pieces = {
 "r":"♜","n":"♞","b":"♝","q":"♛","k":"♚","p":"♟",
 "R":"♖","N":"♘","B":"♗","Q":"♕","K":"♔","P":"♙"," ":""
};

function draw(){
 let t=document.getElementById("board");
 t.innerHTML="";
 for(let i=0;i<8;i++){
  let r=t.insertRow();
  for(let j=0;j<8;j++){
   let c=r.insertCell();
   c.innerHTML=pieces[board[i][j]];
   c.className=((i+j)%2==0)?"w":"b";
   c.onclick=()=>clickCell(i,j);
  }
 }
}

function clickCell(x,y){
 if(!selected){
  selected={x,y};
 } else {
  fetch("/move",{
   method:"POST",
   headers:{"Content-Type":"application/json"},
   body:JSON.stringify({
    sx:selected.x, sy:selected.y,
    ex:x, ey:y
   })
  })
  .then(r=>r.json())
  .then(d=>{
   if(d.success){
    board=d.board;
    turn=d.turn;
    document.getElementById("turn").innerText =
     turn.charAt(0).toUpperCase()+turn.slice(1)+"'s Turn";
    draw();
   }
  });
  selected=null;
 }
}

draw();
</script>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, board=board, turn=turn)

@app.route("/move", methods=["POST"])
def move():
    global turn
    d = request.json
    sx, sy, ex, ey = d["sx"], d["sy"], d["ex"], d["ey"]

    piece = board[sx][sy]
    if piece == " ":
        return jsonify(success=False)

    if turn == "white" and piece.islower():
        return jsonify(success=False)

    if turn == "black" and piece.isupper():
        return jsonify(success=False)

    board[ex][ey] = piece
    board[sx][sy] = " "
    turn = "black" if turn=="white" else "white"

    return jsonify(success=True, board=board, turn=turn)
