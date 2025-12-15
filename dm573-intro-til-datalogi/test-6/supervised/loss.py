
def calculate_loss(a, b, S):
    """
    Calculate the loss function for a linear model.

    Parameters:
    -----------
    a : float
        Slope of the linear model
    b : float
        Intercept of the linear model
    S : list of tuples
        Dataset containing (x, y) pairs

    Returns:
    --------
    float
        The calculated loss value
    """
    n = len(S)
    total_error = 0

    for x_i, y_i in S:
        # Calculate prediction: f(x_i, a, b) = a*x_i + b
        prediction = a * x_i + b

        # Calculate squared error
        error = (prediction - y_i) ** 2
        total_error += error

    # Return average loss
    loss = total_error / n
    return loss

if __name__ == "__main__":
    # Define the dataset
    S = [(2, 3), (4, 8), (6, 7)]

    # Test with some values of a and b
    a = 1.25
    b = 0.5

    loss = calculate_loss(a, b, S)
    print(f"Dataset S: {S}")
    print(f"Parameters: a = {a}, b = {b}")
    print(f"Loss: {loss:.4f}")
