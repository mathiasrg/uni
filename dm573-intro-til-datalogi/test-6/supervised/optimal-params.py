
def find_optimal_parameters(S):
    """
    Find the optimal values of a and b that minimize the loss function.

    Uses the analytical solution derived from setting partial derivatives to zero:
    - b_best = ȳ - a*x̄ (where x̄ and ȳ are the center of mass)
    - a_best = Σ(y_i - ȳ)(x_i - x̄) / Σ(x_i - x̄)²

    Parameters:
    -----------
    S : list of tuples
        Dataset containing (x, y) pairs

    Returns:
    --------
    tuple (a_best, b_best)
        The optimal slope and intercept values
    """
    n = len(S)

    # Calculate center of mass (mean of x and y)
    x_bar = sum(x_i for x_i, y_i in S) / n
    y_bar = sum(y_i for x_i, y_i in S) / n

    # Calculate a_best = Σ(y_i - ȳ)(x_i - x̄) / Σ(x_i - x̄)²
    numerator = sum((y_i - y_bar) * (x_i - x_bar) for x_i, y_i in S)
    denominator = sum((x_i - x_bar) ** 2 for x_i, y_i in S)

    a_best = numerator / denominator

    # Calculate b_best = ȳ - a*x̄
    b_best = y_bar - a_best * x_bar

    return a_best, b_best

if __name__ == "__main__":
    # Define the dataset
    S = [(2, 3), (4, 8), (6, 7)]

    # Find optimal parameters
    a_best, b_best = find_optimal_parameters(S)

    print(f"Dataset S: {S}")
    print(f"\nOptimal parameters:")
    print(f"  a_best = {a_best:.4f}")
    print(f"  b_best = {b_best:.4f}")
