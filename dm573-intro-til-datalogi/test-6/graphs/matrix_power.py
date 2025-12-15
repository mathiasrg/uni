from matrix_mult import multSquareMatrices

def matrix_power(M, power):
    if power < 0:
        raise ValueError("Power must be a non-negative integer")

    n = len(M)

    # Check matrix is square
    for row in M:
        if len(row) != n:
            raise ValueError("Matrix must be square")

    # Identity matrix
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    # Repeated multiplication
    for _ in range(power):
        result = multSquareMatrices(result, M)

    return result

A = [
    [0, 1, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0]
]

print(matrix_power(A, 4))

