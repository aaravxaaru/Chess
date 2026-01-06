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
<body style="text-align:center">
<h1>♟️ Chess</h1>
<h3 id="turn">White's Turn</h3>
<table border="1" style="margin:auto;font-size:40px"></table>

<script>
let board={{ board|tojson }};
let turn="{{ turn }}";
let s=null;
const p={"r":"♜","n":"♞","b":"♝","q":"♛","k":"♚","p":"♟",
"R":"♖","N":"♘","B":"♗","Q":"♕","K":"♔","P":"♙"," ":""};

let t=document.querySelector("table");
function d(){
 t.innerHTML="";
 for(let i=0;i<8;i++){
  let r=t.insertRow();
  for(let j=0;j<8;j++){
   let c=r.insertCell();
   c.innerHTML=p[board[i][j]];
   c.onclick=()=>m(i,j);
  }
 }
}
function m(x,y){
 if(!s)s={x,y};
 else{
 fetch("/move",{method:"POST",headers:{"Content-Type":"application/json"},
 body:JSON.stringify({sx:s.x,sy:s.y,ex:x,ey:y})})
 .then(r=>r.json()).then(d=>{
  if(d.success){
   board=d.board;turn=d.turn;
   document.getElementById("turn").innerText=turn+"'s Turn";
   d();
  }
 });
 s=null;
 }
}
d();
</script>
</body>
</html>
"""

@app.route("/")
def i():
    return render_template_string(HTML, board=board, turn=turn)

@app.route("/move", methods=["POST"])
def move():
    global turn
    d=request.json
    sx,sy,ex,ey=d["sx"],d["sy"],d["ex"],d["ey"]
    pc=board[sx][sy]
    if pc==" ": return jsonify(success=False)
    if turn=="white" and pc.islower(): return jsonify(success=False)
    if turn=="black" and pc.isupper(): return jsonify(success=False)
    board[ex][ey]=pc; board[sx][sy]=" "
    turn="black" if turn=="white" else "white"
    return jsonify(success=True, board=board, turn=turn)
