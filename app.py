from flask import Flask,render_template,request

app=Flask(__name__)
@app.route("/",methods=["GET", "POST"])

def index():
    return render_template("index.html")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Error: no code provided"
    return code

if __name__=="__main__":
    app.run(debug=True)