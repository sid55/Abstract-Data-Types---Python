import numpy as np
import timeit
import scipy
from matplotlib import pyplot as plt
import random

#MERGESORT ALGORITHM
def mergeSort(myArray, start, end):
    if start < end:
        middle = int((start+end)/2)
        mergeSort(myArray,start,middle)
        mergeSort(myArray,middle+1,end)
        merge(myArray,start,end)

def merge(myArray,start,end):
    i = start
    middle = int((start+end)/2)
    j = middle+1
    tempSize = end-start+1
    temp = np.empty(tempSize,int)
    k = 0

    while i <= middle and j <= end:
        if myArray[i] <= myArray[j]:
            temp[k] = myArray[i]
            i = i+1
            k = k+1
        else:
            temp[k] = myArray[j]
            j = j+1
            k = k+1

    while i <= middle:
        temp[k] = myArray[i]
        i = i+1
        k = k+1

    while j <= end:
        temp[k] = myArray[j]
        j = j+1
        k = k+1

    for x in range(len(temp)):
        myArray[start+x] = temp[x]
        
##############################################

#AVERAGE CASE MERGESORT
np.random.seed(54)
alistMergeAvg = np.arange(1000, dtype=float)
n = 1
p = 0
for x in range(len(alistMergeAvg)):
    t = timeit.Timer(lambda:mergeSort(np.random.permutation(n),0,p))
    res = t.repeat(repeat = 1000, number = 1)
    l = scipy.mean(res)
    alistMergeAvg[x] = scipy.mean(res)
    n = n+1
    p = p+1

################################################

plt.figure(1)
plt.plot(alistMergeAvg)
plt.show()