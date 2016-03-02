import numpy as np
import timeit
import scipy
from matplotlib import pyplot as plt
import random

#INSERTION SORT ALGORITHM
def insertionSort(myArray):
    for j in range(1,len(myArray)):
        key = myArray[j]
        i = j-1
        while i>=0 and myArray[i]>key:
            myArray[i+1] = myArray[i]
            i = i-1
        myArray[i+1] = key


#AVERAGE CASE INSERTION SORT
np.random.seed(54)
alistInsertionAvg = np.arange(1000, dtype=float)
n = 1
p = 0
for x in range(len(alistInsertionAvg)):
    t = timeit.Timer(lambda:insertionSort(np.random.permutation(n)))
    res = t.repeat(repeat = 1000, number = 1)
    l = scipy.mean(res)
    alistInsertionAvg[x] = scipy.mean(res)
    n = n+1
    p = p+1


plt.figure(1)
plt.plot(alistInsertionAvg)
plt.show()