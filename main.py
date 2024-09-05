#Q4 + Q5 (Numerical Analysis- section 1)

import numpy as np

# a function to validate matrices
# 1. Checking if the entered array is a square matrix or not (Note [0]:Rows/ [1] Columns)
def gaussian_elimination(matrix_a, matrix_b):
    if matrix_a.shape[0] != matrix_a.shape[1]:
        print("NOT A SQUARE MATRIX!!")
        return
    # checks the b matrix if it contains 1 column and the same rows as the A matrix
    if matrix_b.shape[1] > 1 or matrix_b.shape[0] != matrix_a.shape[0]:
        print("Constant vector might consist of more than one column or has more rows than the matrix")
        return

    print("ACCEPTED!")

    # 1. we need to concatenate A metrix with the B matrix to get the augmented matrix
    augmented_matrix = np.concatenate((matrix_a, matrix_b), axis=1, dtype=float)  # data type integer could cause errors in truncating numbers
    print("Your Augmented Matrix : \n", augmented_matrix)

    n = len(matrix_b)
    m = n - 1
    i = 0
    j = i - 1
    while i < n:

        if augmented_matrix[i, i] == 0.0:
            print("Main diagonal contains zeros")
            return

        for j in range(i + 1, n):
            scalar = augmented_matrix[j, i] / augmented_matrix[i, i]
            augmented_matrix[j] = augmented_matrix[j] - (scalar * augmented_matrix[i])
            print("\n*************************")
            print(augmented_matrix)


        i = i + 1

    # Now we solve for x1,x2,x3
    x = np.zeros(n)  # used for generating the solution vector

    x[m] = augmented_matrix[m][n] / augmented_matrix[m][m]
    # The bottom row is the pivotal row

    # n = 4/ the loop proceeds until it reaches the last row and decrements by 1/n=2
    for k in range(n-2, -1, -1):
        x[k] = augmented_matrix[k, n]

        # backwards substitution
        for j in range(k+1, n):
            x[k] = x[k] - augmented_matrix[k, j] * x[j]

        x[k] = x[k] / augmented_matrix[k, k]

    print("*************************")
    for c in range(n):
        print("X", c+1, "=", x[c])

A = np.array([[2,1,-1],[-3,-1,2],[-2,1,2]])
B = np.array([[8],[-11],[-3]])

gaussian_elimination(A,B)

