import numpy as np
import timeit
import scipy
import matplotlib.pyplot as plt

#PROBLEM 1
#This method uses brute force to calculate the product of
#an n x n matrix with a vector of size n
def matmult (A,x):
   n = len(x)
   b = np.arange(len(A))
   for i in range (0,len(A)):
       temp = 0
       for j in range (0,n):
           temp += A[i][j] * x[j]
       b[i] = temp    
   return (b)

#PROBLEM 2
#This method recursively calls itself in order for it to 
#create a matrix given k. The matrix created from this 
#method will be a hadamard matrix of size 2^k x 2^k
def hadmat (k):
    if k == 0:
        return np.array([[1]])
    elif k == 1:
        return np.array([[1, 1], [1,-1]])
    else:
        temp = hadmat(k-1)
        new = np.concatenate((temp,temp), axis = 1)
        new2 = np.concatenate((temp,-temp), axis = 1)
        final = np.concatenate((new,new2), axis = 0)
        return(final)

#PROBLEM 4
#This method recursively calls itself with subarrays and subvectors.
#It calculates the product of a hadamard matrix of size n x n with 
#a vector of size n.
def hadmatmult(H,x):
    n = len(x)//2
    x1 = x[0:n]
    x2 = x[n:len(x)]
    if len(H) == 2:
        return np.array([(H[0,0]*x1[0] + H[0,1]*x2[0]),(H[1,0]*x1[0] + H[1,1]*x2[0])])
    else:
        temp = hadmatmult(H[0:len(x1),0:len(x1)],x1)
        temp2 = hadmatmult(H[0:len(x1),len(x1):len(x)],x2)
        temp3 = temp
        temp4 =-1*temp2
        created = temp + temp2
        created2 = temp3 + temp4
        final = np.concatenate((created,created2), axis = 1)
        return final 

#PROBLEM 5
#This is code for creating the two plots onto the 
#graph        
# k = 1
# arraysize = 12
# m = [0] * arraysize
# temp = [0] * arraysize
# temp2 = [0] * arraysize
# N = [0] * arraysize
# for k in range(1,13):
#     np.random.seed(10)
#     m = np.random.randint(1,10, 2**k)
#     t = timeit.Timer(lambda:matmult(hadmat(k),m))
#     l = scipy.mean(t.repeat(repeat = 1, number = 1))
#     temp[k-1] = l
#     t2 = timeit.Timer(lambda:hadmatmult(hadmat(k),m))
#     l2 = scipy.mean(t2.repeat(repeat = 1, number = 1))
#     temp2[k-1] = l2
#     N[k-1] = 2**k
# plt.figure()
# plt.plot(N,temp,label = "matmult")
# plt.plot(N, temp2, label = "hadmatmult" )
# plt. xlabel('n')
# plt.ylabel('time')
# plt.title('Problem 5 Graph')
# plt.legend(loc = 'upper left')
# plt.show()