from flask import Flask, render_template, request
import json
import requests
import html

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("form2.html")

@app.route("/result")
def result():
    keyword = request.args.get("keyword")
    req = requests.get("https://ja.dbpedia.org/data/"+keyword+".json")
    jsn = json.loads(req.text)
    abstract = jsn["http://ja.dbpedia.org/resource/"+keyword]["http://www.w3.org/2000/01/rdf-schema#comment"][0]["value"]
    return "<h1>検索結果</h1>\n" + html.escape(abstract)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)