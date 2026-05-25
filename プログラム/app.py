from flask import Flask, render_template, request, redirect, jsonify
import json

app = Flask(__name__)

@app.route("/")
def home():
    f = open("graph.json", "r")
    jsn = f.read()
    f.close()
    if jsn == "":
        sense = {}
        sense["graph"] = []
        f = open("graph.json", "w")
        f.write(json.dumps(sense))
        f.close()
    f = open("control.json", "r")
    jsn = f.read()
    f.close()
    if jsn == "":
        con = {}
        con["temp"] = 0
        con["cont"] = "none"
        f = open("control.json", "w")
        f.write(json.dumps(con))
        f.close()
    return render_template("index.html")

@app.route("/reset")
def reset():
    con = {}
    con["temp"] = 0
    con["cont"] = "none"
    f = open("control.json", "w")
    f.write(json.dumps(con))
    f.close()
    sense = {}
    sense["graph"] = []
    f = open("graph.json", "w")
    f.write(json.dumps(sense))
    f.close()
    return redirect("..")

@app.route("/sense", methods=["POST"])
def sense():
    temp = request.form["temp"]
    f = open("graph.json", "r")
    jsn = f.read()
    f.close()
    dic = json.loads(jsn)
    dic["graph"].append(float(temp))
    f = open("graph.json", "w")
    f.write(json.dumps(dic))
    f.close()
    f = open("control.json", "r")
    jsn = f.read()
    f.close()
    dic = json.loads(jsn)
    dic["temp"] = float(temp)
    f = open("control.json", "w")
    f.write(json.dumps(dic))
    f.close()
    return "200 OK"

@app.route("/con", methods=["POST"])
def control():
    con = request.form["con"]
    f = open("control.json", "r")
    jsn = f.read()
    f.close()
    dic = json.loads(jsn)
    dic["cont"] = con
    f = open("control.json", "w")
    f.write(json.dumps(dic))
    f.close()
    return redirect("..")

@app.route("/api-graph")
def api_graph():
    f = open("graph.json", "r")
    jsn = f.read()
    f.close()
    return jsonify(json.loads(jsn))

@app.route("/api-control")
def api_control():
    f = open("control.json", "r")
    jsn = f.read()
    f.close()
    return jsonify(json.loads(jsn))
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")
