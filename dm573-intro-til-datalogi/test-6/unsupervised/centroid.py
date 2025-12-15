
def calculate_centroid(C):
    """
    Calculate the centroid of a cluster C.

    The centroid μ_C is calculated as:
    μ_C = (1 / |C|) · Σ(o∈C) o

    Parameters:
    -----------
    C : list of tuples or list of lists
        A dataset containing points, where each point is a tuple or list of coordinates
        Example: [(2, 3), (5, 5), (4, 1)]

    Returns:
    --------
    tuple : The centroid coordinates

    Example:
    --------
    >>> C = [(2, 3), (5, 5), (4, 1)]
    >>> calculate_centroid(C)
    (3.6666666666666665, 3.0)
    """
    if not C:
        raise ValueError("Dataset C cannot be empty")

    # Get the number of points in the cluster
    cardinality = len(C)

    # Get the dimensionality (number of coordinates per point)
    dimensions = len(C[0])

    # Initialize centroid coordinates
    centroid = []

    # Calculate each dimension of the centroid
    for dim in range(dimensions):
        # Sum all values in this dimension
        dim_sum = sum(point[dim] for point in C)
        # Divide by cardinality to get the mean
        centroid.append(dim_sum / cardinality)

    return tuple(centroid)

if __name__ == "__main__":
    # Test with the example dataset
    C = [(2, 3), (5, 5), (4, 1)]
    centroid = calculate_centroid(C)
    print(f"Dataset: {C}")
    print(f"Centroid: {centroid}")
    print(f"Centroid (rounded): ({centroid[0]:.2f}, {centroid[1]:.2f})")
