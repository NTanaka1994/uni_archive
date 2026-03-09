import requests
import json

param = {}
param["method"] = "searchByPostal"
param["postal"] = "1840002"
req = requests.get("https://geoapi.heartrails.com/api/json", param)
jsn = json.loads(req.text)