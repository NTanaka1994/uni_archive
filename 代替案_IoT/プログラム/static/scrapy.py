import requests

req = requests.get("https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns@next/dist/chartjs-adapter-date-fns.bundle.min.js")
text = req.text

f = open("chartjs-adapter-date-fns.bundle.min.js", "w")
f.write(text)
f.close()