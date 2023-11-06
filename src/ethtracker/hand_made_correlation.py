import numpy as np
# from src.ethtracker.decorators import light_print_time_to_work


# @light_print_time_to_work
def calculate_correlation(x, y):
    # check length of the arrays
    if len(x) != len(y):
        raise ValueError("Length of x and y are not equal")
    if len(x) < 5:
        print("Needs 5 members of lists for calculating")
        return None

    # Convert to arrays NumPy
    x_array = np.array(x)
    y_array = np.array(y)

    # Solve average values
    x_mean = np.mean(x_array)
    y_mean = np.mean(y_array)

    try:
        # calculate the sum of multiplications of deviations from average values
        numerator = np.sum((x_array - x_mean) * (y_array - y_mean))

        # calculate the sum of squared deviations from the average values
        denominator = np.sqrt(np.sum((x_array - x_mean) ** 2) * np.sum((y_array - y_mean) ** 2))

        # Calculate linear correlation
        correlation_coefficient = numerator / denominator
    except:
        print("Some errors")
        correlation_coefficient = None

    return correlation_coefficient


if __name__ == '__main__':
    x_values = [1.2, 1.5, 1.8, 2.1, 2.4]
    y_values = [0.9, 1.2, 1.5, 1.8, 2.1]

    correlation = calculate_correlation(x_values, y_values)
    print("Correlation coefficient:", correlation)
