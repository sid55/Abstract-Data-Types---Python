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
        
        
#MERGESORT EXAMPLE EVEN NUMBER     
alistMerge = np.array([3,4,2,6,8,7])
mergeSort(alistMerge,0,5)
print(alistMerge)

#MERGESORT EXAMPLE ODD NUMBER     
alistMerge2 = np.array([3,4,2,6,8,7,11])
mergeSort(alistMerge2,0,6)
print(alistMerge2)

#INSERTIONSORT EXAMPLE EVEN NUMBER     
alistInsertion = np.array([3,4,2,6,8,7])
mergeSort(alistInsertion,0,5)
print(alistInsertion)

#INSERTIONSORT EXAMPLE ODD NUMBER     
alistInsertion2 = np.array([3,4,2,6,8,7,11])
mergeSort(alistInsertion2,0,6)
print(alistInsertion2)
  