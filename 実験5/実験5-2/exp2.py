import requests
import json
from collections import deque

def width(jsn, var=""):
    queue = deque([(jsn, var)])
    while queue:
        node, var = queue.popleft()
        if isinstance(node, dict):
            for key in node:
                queue.append((node[key], var+"[\""+key+"\"]"))
        elif isinstance(node, list) and node != []:
            for i in range(len(node)):
                queue.append((node[i], var+"["+str(i)+"]"))
        else:
            if "法政大学（ほうせいだいがく、英語: Hosei University）は" in str(node):
                print(var+"="+str(node))
            pass

def depth(jsn, var=""):
    if isinstance(jsn, dict):
        for row in jsn:
            depth(jsn[row], var=var+"[\""+row+"\"]")
    elif isinstance(jsn, list) and jsn != []:
        for i in range(len(jsn)):
            depth(jsn[i], var=var+"["+str(i)+"]")
    else:
        if "法政大学（ほうせいだいがく、英語: Hosei University）は" in str(jsn):
            print(var+"="+str(jsn))
        pass

req = requests.get("https://ja.dbpedia.org/data/法政大学.json")
jsn = json.loads(req.text)
depth(jsn, "data")