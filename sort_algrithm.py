import numpy as np

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
    pivot = a[(first + last) // 2]
    print(pivot)
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
        print(a)
    if first < (i - 1):
        quick(a, first, i-1)
    if (j + 1) < last:
        quick(a, j+1, last)

def create_array():
    rng = np.random.default_rng()
    a = []
    while len(a)<10:
        tmp = rng.integers(10)
        if tmp not in a:
            a.append(tmp)
    return a
a = create_array()
print(a)
quick(a, 0, 9)
