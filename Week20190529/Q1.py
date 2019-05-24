#!usr/bin/env python3

import numpy as np
input_matrix = np.array([
    [1, 0.3, 0.3, 0.3], 
    [0.3, 1, 0.3, 0.3],
    [0.3, 0.3, 1, 0.3],
    [0.3, 0.3, 0.3, 1]
    ])

def cholesky_decomp(correlationmatrix):
    cholmat = np.zeros_like(correlationmatrix)
    for i in range(len(cholmat)):
        for j in range(i+1):
            if i==j:
                #this computes the diagonal values
                diag = correlationmatrix[i,i] - np.sum(np.square(cholmat[i,:i]))
                #because you cannot sqrt a negative number:
                if diag<0:
                    return 0.0
                cholmat[i,i] = np.sqrt(diag)
            else:
                #computing the rest of the matrix
                cholmat[i,j] = (correlationmatrix[i,j] - np.sum(cholmat[i,:j]*cholmat[j,:j]))/cholmat[j,j]
    return cholmat

cholesky_from_function = cholesky_decomp(input_matrix)
cholesky_from_np = np.linalg.cholesky(input_matrix)
check = np.allclose(cholesky_from_function,cholesky_from_np)

print("\nCorrelation matrix:")
print(input_matrix)
print("\nCholesky from function:")
print(cholesky_from_function)
print("\nCholesky from numpy:")
print(cholesky_from_np)
print("\nAre the two cholesky matrices essentially identical??")
print(check)