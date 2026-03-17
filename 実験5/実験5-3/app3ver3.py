from flask import jsonify, Flask, send_file, request
from urllib.parse import quote
import glob
import pandas as pd
import httpx
import asyncio
import html
import socket
import os

app = Flask(__name__)

@app.route("/")
async def home():
    df = pd.read_csv("node.csv")
    res = "<table border=\"1\">"
    async with httpx.AsyncClient(timeout=3.0) as client:
        tasks = []
        for i in range(len(df.values)):
            tasks.append(client.get("http://"+df.values[i][0]+"/files"))
        responses = await asyncio.gather(*tasks, return_exceptions=True)
    for response in responses:
        if isinstance(response, Exception):
            continue
        jsn = response.json()
        res += "<tr><td>" + list(jsn)[0] + "</td><td>"
        for i in range(len(jsn[list(jsn)[0]])):
            res += "<a href=\"http://" + list(jsn)[0] + "/download?name=" + quote(jsn[list(jsn)[0]][i].replace("./files\\", "")) + "\">" + html.escape(jsn[list(jsn)[0]][i].replace("./files\\", "")) + "</a><br>\n"
        res += "</td></tr>\n"
    res += "</table>"
    return res

@app.route("/files")
def files():
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    jsn = {ip : glob.glob("./files/*")}
    return jsonify(jsn)

@app.route("/download")
def download():
    file = request.args.get("name")
    return send_file("files/"+os.path.basename(file))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)