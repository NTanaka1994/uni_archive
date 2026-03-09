from flask import Flask, render_template, request
import json
import requests

app = Flask("__name__")

@app.route("/")
def home():
    return render_template("form1.html")

@app.route("/geo")
def geo():
    postnum = request.args.get("postnum")
    param = {}
    param["method"] = "searchByPostal"
    param["postal"] = postnum
    req = requests.get("https://geoapi.heartrails.com/api/json", param)
    jsn = json.loads(req.text)
    pref = jsn["response"]["location"][0]["prefecture"]
    city = jsn["response"]["location"][0]["city"]
    town = jsn["response"]["location"][0]["town"]
    return "<h1>出力結果</h1>" + "\n" + pref + city + town

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)