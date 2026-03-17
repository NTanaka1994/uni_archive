from flask import Flask, jsonify
import pandas as pd
import httpx
import asyncio
import html

app = Flask(__name__)

@app.route("/")
async def home():
    df = pd.read_csv("node.csv")
    res = "<table border=\"1\">"
    res += "<tr><td>学生証番号</td><td>名前</td><td>所属</td></tr>\n"
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(len(df.values)):
            tasks.append(client.get("http://"+df.values[i][0]+"/api"))
        responses = await asyncio.gather(*tasks, return_exceptions=True)
    for response in responses:
        if isinstance(response, Exception):
            continue
        jsn = response.json()
        res += "<tr><td>" + html.escape(jsn["num"]) + "</td><td>" + html.escape(jsn["name"]) + "</td><td>" + html.escape(jsn["in"]) + "</td></tr>\n"
    res += "</table>"
    return res

@app.route("/api")
def result():
    api = {}
    api["num"] = "14X3111"
    api["name"] = "田中直哉"
    api["in"] = "理工学部応用情報工学科"
    return jsonify(api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)