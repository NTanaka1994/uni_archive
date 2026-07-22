from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def _read_json(path: str, default: dict):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(json.dumps(default))
        return default
    with open(path, "r") as f:
        txt = f.read()
    if txt.strip() == "":
        with open(path, "w") as f:
            f.write(json.dumps(default))
        return default
    try:
        return json.loads(txt)
    except Exception:
        with open(path, "w") as f:
            f.write(json.dumps(default))
        return default


def _write_json(path: str, obj: dict):
    with open(path, "w") as f:
        f.write(json.dumps(obj))


@app.get("/")
async def home(request: Request):
    _read_json("graph.json", {"graph": []})
    _read_json("control.json", {"temp": 0, "cont": "none"})
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/reset")
async def reset():
    _write_json("control.json", {"temp": 0, "cont": "none"})
    _write_json("graph.json", {"graph": []})
    return RedirectResponse(url="/")


@app.post("/sense")
async def sense(temp: float = Form(...)):
    g = _read_json("graph.json", {"graph": []})
    g["graph"].append(float(temp))
    _write_json("graph.json", g)

    c = _read_json("control.json", {"temp": 0, "cont": "none"})
    c["temp"] = float(temp)
    _write_json("control.json", c)
    return PlainTextResponse("200 OK")


@app.post("/con")
async def control(con: str = Form(...)):
    c = _read_json("control.json", {"temp": 0, "cont": "none"})
    c["cont"] = con
    _write_json("control.json", c)
    return RedirectResponse(url="/")


@app.get("/api-graph")
async def api_graph():
    g = _read_json("graph.json", {"graph": []})
    return JSONResponse(content=g)


@app.get("/api-control")
async def api_control():
    c = _read_json("control.json", {"temp": 0, "cont": "none"})
    return JSONResponse(content=c)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
