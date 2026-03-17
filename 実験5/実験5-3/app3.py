from flask import Flask, jsonify
import json
import requests
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    df = pd.read_csv("node.csv")
    res = "<table border=\"1\">"
    res += "<tr><td>学生証番号</td><td>名前</td><td>所属</td></tr>\n"
    for i in range(len(df.values)):
        req = requests.get("http://" + df.values[i][0] +"/api")
        jsn = json.loads(req.text)
        res += "<tr><td>" + jsn["num"] + "</td><td>" + jsn["name"] + "</td><td>" + jsn["in"] + "</td></tr>\n" 
    return res

@app.route("/api")
def result():
    api = {}
    api["num"] = "14X3111"
    api["name"] = "hoge"
    api["in"] = "理工学部応用情報工学科"
    return jsonify(api)
    
if __name__ == "__main__":

    app.run(host="0.0.0.0", port=80)
