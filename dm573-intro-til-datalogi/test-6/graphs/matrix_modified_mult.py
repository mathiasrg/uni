def multModSquareMatrices(M, N):
    size = len(M)
    result = [[float('inf') for x in range(size)] for y in range(size)]

    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] = min(result[i][j], M[i][k] + N[k][j])

    return result
