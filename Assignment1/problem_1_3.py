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

#INSERTION SORT ALGORITHM
def insertionSort(myArray):
    for j in range(1,len(myArray)):
        key = myArray[j]
        i = j-1
        while i>=0 and myArray[i]>key:
            myArray[i+1] = myArray[i]
            i = i-1
        myArray[i+1] = key

##############################################

#MERGESORT ALGORITHM FOR MAKING WORST ARRAY
def newSort(myArray, number):
    if len(myArray) == 2:
        temp = myArray[1]
        myArray[1] = myArray[0]
        myArray[0] = temp
    elif len(myArray) == 1:
        return 1

    size = int(number/2)
    if number%2 == 0:
        leftArray = np.arange(size)
        rightArray = np.arange(size)
    elif number%2 != 0:
        leftArray = np.arange( size + 1)
        rightArray = np.arange( size )

    k = 0
    i = 0
    a = 0
    while a < len(leftArray):
        leftArray[k] = myArray[i]
        i = i+2
        k = k+1
        a = a+1

    b = 0
    k = 0
    i = 1
    while b < len(rightArray):
        rightArray[k] = myArray[i]
        i = i+2
        k = k+1
        b = b+1

    newSort(leftArray,len(leftArray))
    newSort(rightArray,len(rightArray))
    newMerge(myArray,leftArray,rightArray)

def newMerge(myArray,leftArrayNew,rightArrayNew):
    i = 0
    for x in range(len(leftArrayNew)):
        myArray[i] = leftArrayNew[x]
        i = i+1
    for y in range(len(rightArrayNew)):
        myArray[i] = rightArrayNew[y]
        i = i+1

###################################################

#For all the cases shown below I am using the max number of elements 
#to be 1000. If I exceed 1000 elements, the program is taking too long to 
#compute all the times. That is why I have chosen the max number of 
#elements to be 1000.

#BEST CASE INSERTION SORT
alistInsertionBest = np.arange(1000, dtype=float)
n = 1
p = 0
for x in range(len(alistInsertionBest)):
    alistTemp = np.arange(n)
    t = timeit.Timer(lambda:insertionSort(alistTemp))
    res = t.repeat(repeat = 1, number = 1)
    l = scipy.mean(res)
    alistInsertionBest[x] = scipy.mean(res)
    n = n+1
    p = p+1
#print(alistInsertionBest)

#WORST CASE INSERTION SORT
alistInsertionWorst = np.arange(1000, dtype=float)
n = 1
p = 0
for x in range(len(alistInsertionWorst)):
    alistTemp = np.arange(n)
    alistBackwards = alistTemp[::-1]
    t = timeit.Timer(lambda:insertionSort(alistBackwards))
    res = t.repeat(repeat = 1, number = 1)
    l = scipy.mean(res)
    alistInsertionWorst[x] = scipy.mean(res)
    n = n+1
    p = p+1
#print(alistInsertionWorst)

#########################################################

#BEST CASE MERGESORT        
alistMergeBest = np.arange(1000, dtype=float)
n = 1
p = 0
for x in range(len(alistMergeBest)):
    alistTemp = np.arange(n)
    t = timeit.Timer(lambda:mergeSort(alistTemp,0,p))
    res = t.repeat(repeat = 1, number = 1)
    l = scipy.mean(res)
    alistMergeBest[x] = scipy.mean(res)
    n = n+1
    p = p+1
#print(alistMergeBest)

    
#WORST CASE MERGESORT
alistMergeWorst = np.arange(1000, dtype=float)
n = 1
p = 0
for x in range(len(alistMergeWorst)):
    alist = np.arange(n)
    newSort(alist,len(alist))
    t = timeit.Timer(lambda:mergeSort(alist,0,p))
    res = t.repeat(repeat = 1, number = 1)
    l = scipy.mean(res)
    alistMergeWorst[x] = scipy.mean(res)
    n = n+1
    p = p+1
#print(alistMergeWorst)