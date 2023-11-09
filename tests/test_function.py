from src.ethtracker.functions import detect_best_timing
from config.config import POSSIBLE_TIMINGS


def test_detect_best_timing(mock_ex_rates):
    a, b, x = detect_best_timing(mock_ex_rates, mock_ex_rates, POSSIBLE_TIMINGS)
    assert a == POSSIBLE_TIMINGS[0]['interval']
    assert b == POSSIBLE_TIMINGS[0]['num_of_samples']
    assert x == 1.0


def test_detect_best_timing_ex(mock_ex_rates, mock_ex_rates_exception):
    a, b, x = detect_best_timing(mock_ex_rates, mock_ex_rates_exception, POSSIBLE_TIMINGS)
    assert a == POSSIBLE_TIMINGS[0]['interval']
    assert b == POSSIBLE_TIMINGS[0]['num_of_samples']
    assert x == 0.0
