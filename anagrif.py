import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("picture.csv")
data = df.values
A = 600
B = 600
W = 20
N = 5000
M = 1
rng = np.random.default_rng()
plt.figure(figsize=(6, 6))
xl = []
xr = []
y = []
for i in range(N):
    xp = rng.uniform(0, len(data[0]))
    yp = rng.uniform(0, len(data))
    zp = M * data[int(yp)][int(xp)]
    xp = xp - len(data[0]) / 2
    yp = yp - len(data) / 2
    xl.append((+A*W+B*xp+W*zp)/(A+B-zp))
    xr.append((+A*W+B*xp-W*zp)/(A+B-zp))
    y.append( B * yp / (A + B - zp))
plt.scatter(xl, y, color="#EE7800", s=1)
plt.scatter(xr, y, color="#00FFFF", s=1)
plt.xlim(-0.25*len(data[0]), 0.25*len(data[0]))
plt.ylim(-0.25*len(data), 0.25*len(data))
plt.savefig("anagrif.png")
plt.show()