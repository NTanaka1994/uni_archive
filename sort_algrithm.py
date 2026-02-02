import numpy as np
import matplotlib.pyplot as plt
from time import time

def babble(a, length):
    for i in range(length-1):
        for j in range(length-i-1):
            if a[j+1] < a[j]:
                temp = a[j]
                a[j] = a[j+1]
                a[j+1] = temp
            print(a)
            
def insertion(a, n):
    for i in range(n):
        temp = a[i]
        j = i - 1
        while j >= 0 and a[j] > temp:
            a[j+1] = a[j]
            j = j - 1
        a[j+1] = temp
        print(a)
        
def quick(a, first, last):
    cnt = 0
    pivot = a[(first + last) // 2]
    #print(pivot)
    #print(a[first:last+1])
    i = first
    j = last
    while(True):
        while a[i] < pivot:
            i = i + 1
        while pivot < a[j]:
            j = j - 1
        if i >= j:
            break
        temp = a[i]
        a[i] = a[j]
        a[j] = temp
        cnt = cnt + 1
        i = i + 1
        j = j - 1
        #print(a[first:last+1])
        #print(a)
    if first < (i - 1):
        cnt = cnt + quick(a, first, i-1)
    if (j + 1) < last:
        cnt = cnt + quick(a, j+1, last)
    #print(a)
    return cnt

def rand_array(n):
    rng = np.random.default_rng()
    a = []
    while len(a)<n:
        tmp = rng.integers(n)
        if tmp not in a:
            a.append(tmp)
    return a
def voly_array(n):
    a = []
    for i in range(n, 0, -2):
        a.append(i)
    for i in range(1, n, 2):
        a.append(i)
    return a

def voly2_array(n):
    a = []
    for i in range(n//2, n):
        a.append(i)
    for i in range(0, n//2):
        a.append(i)
    return a

def saw_array(n):
    a = []
    for i in range(1, n//2+1):
        a.append(i)
        a.append(n-(i-1))
    return a
cnt_v = []
cnt_v2 = []
cnt_s = []
volly = []
volly2 = []
saw = []
val = []
for i in range(10, 10000, 100):
    val.append(i)
    a = voly_array(i)
    past = time()
    cnt_v.append(quick(a, 0, len(a)-1))
    now = time()
    volly.append(now-past)
    a = voly2_array(i)
    past = time()
    cnt_v2.append(quick(a, 0, len(a)-1))
    now = time()
    volly2.append(now-past)
    a = saw_array(i)
    past = time()
    cnt_s.append(quick(a, 0, len(a)-1))
    now = time()
    saw.append(now-past)
    
plt.scatter(val, volly, label="Volley(V-pattern)")
plt.scatter(val, volly2, label="Volley(High2Low)")
plt.scatter(val, saw, label="saw")
plt.legend()
plt.xlabel("Number of elements")
plt.ylabel("Time(s)")
plt.savefig("quicksort_time.png")
plt.show()

plt.scatter(val, cnt_v, label="Volley(V-pattern)")
plt.scatter(val, cnt_v2, label="Volley(High2Low)")
plt.scatter(val, cnt_s, label="saw")
plt.legend()
plt.xlabel("Number of elements")
plt.ylabel("Number of swap")
plt.savefig("quicksort_swap.png")
plt.show() 

#a = voly2_array(10)
#a = [10, 0, 9, 1, 8, 2, 7, 3, 6, 4, 5]
#a = [10, 8, 6, 4 , 2, 0, 1, 3, 5, 7, 9]
#a = saw_array(10)
#print(a)
#quick(a, 0, len(a)-1)
