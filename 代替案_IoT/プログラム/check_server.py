import time
import urllib.request

url = 'http://127.0.0.1:8000/api-control'
for i in range(20):
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            print(r.read().decode())
            break
    except Exception as e:
        time.sleep(0.5)
else:
    print('failed to reach server')
