from flask import Flask, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
<title>Guess the Number</title>
<style>
body{
font-family:Arial;
background:#1e293b;
color:white;
text-align:center;
padding-top:80px;
}
button{
padding:10px 20px;
font-size:18px;
}
</style>
</head>
<body>

<h1>🎮 Welcome to My EKS Game</h1>

<p>Click the button to generate a random number.</p>

<button onclick="play()">Play</button>

<h2 id="result"></h2>

<script>
function play(){
let num=Math.floor(Math.random()*100)+1;
document.getElementById("result").innerHTML="Your Lucky Number: "+num;
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
