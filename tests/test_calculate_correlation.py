from src.ethtracker.hand_made_correlation import calculate_correlation
import pytest

def test_calc_correlation():
    x_values = [1.2, 1.5, 1.8, 2.1, 2.4]
    y_values = [0.9, 1.2, 1.5, 1.8, 2.1]
    correlation = calculate_correlation(x_values, y_values)
    # print("Correlation coefficient:", correlation)
    assert correlation == 1.0

    x_values = [1.2, 1.5, 1.8, 2.1, 2.4]
    y_values = [0.9, 1.2, 1.5, 1.8, 2.8]
    correlation = calculate_correlation(x_values, y_values)
    assert correlation == 0.9529257800132619

    x_values = [1.2, 1.5, 1.8, 2.1, 2.4]
    y_values = [0.9, 1.2, 1.5, 1.8]
    with pytest.raises(ValueError):
        calculate_correlation(x_values, y_values)


    x_values = [1.2, 1.5, 1.8, 2.1]
    y_values = [0.9, 1.2, 1.5, 1.8]
    correlation = calculate_correlation(x_values, y_values)
    assert correlation == None

    x_values = [1.0, 1.0, 1.0, 1.0, 1.0]
    y_values = [1.0, 1.0, 1.0, 1.0, 1.0]
    correlation = calculate_correlation(x_values, y_values)
    assert correlation == 1.0
