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

a = [7, 4, 6, 2, 3, 5, 1, 9, 8, 0]
print(a)
insertion(a, 10)