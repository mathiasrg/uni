def multSquareMatrices(M, N):
    size = len(M)
    result = [[0 for x in range(size)] for y in range(size)]

    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] = result[i][j] + M[i][k] * N[k][j]

    return result

M = [
    [1, 2, 3],
    [4, 5, 6]
]

N = [
    [7, 8],
    [9, 10],
    [11, 12]
]

# Multiply M and N
result = multSquareMatrices(M, N)
