import numpy as np


def calculate_correlation(x, y):
    """ calculate coefficient correlation between x and y loads"""
    # check length of the arrays
    if len(x) != len(y):
        raise ValueError("Length of x and y are not equal")
    if len(x) < 5:
        print("Needs at least 5 members of arrays for calculating")
        return None

    # Convert to arrays NumPy
    x_array = np.array(x)
    y_array = np.array(y)

    # Solve average values
    x_mean = np.mean(x_array)
    y_mean = np.mean(y_array)

    # calculate the sum of multiplications of deviations from average values
    numerator = np.sum((x_array - x_mean) * (y_array - y_mean))

    # calculate the sum of squared deviations from the average values
    denominator = np.sqrt(np.sum((x_array - x_mean) ** 2) * np.sum((y_array - y_mean) ** 2))

    # Calculate linear correlation
    if denominator == 0:
        correlation_coefficient = 1.0
    else:
        correlation_coefficient = numerator / denominator

    return correlation_coefficient
