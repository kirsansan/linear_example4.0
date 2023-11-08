import numpy as np

from src.ethtracker.eth_tracker import Prediction
from config.config import TIME_THRESHOLD


def test_add_to_floating_tail(predict):
    """will delete first observation"""
    # TIME_THRESHOLD = 200
    response = predict.add_to_floating_tail(TIME_THRESHOLD + 400, 6)
    assert predict.floating_tail == [{'time': 500, 'value': 5}, {'time': TIME_THRESHOLD + 400, 'value': 6}]
    assert response == 5


def test_calculate_influence(predict):
    """if all fluctuations of X are 2 times greater than Y - we have to get 0.5"""
    predict.history_btc = np.array([102.0, 104.0, 106.0, 100.0, 102.0, 106.0, 116.0]).astype(float)
    predict.history_eth = np.array([51.0, 52.0, 53.0, 50.0, 51.0, 53.0, 58.0]).astype(float)
    response = predict.calculate_influence()
    assert round(response, 1) == 0.5


def test_get_data(predict, mock_ex_rates):
    predict.requester_btc = mock_ex_rates
    predict.requester_eth = mock_ex_rates
    predict.get_data()
    assert predict.history_btc == [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0]
    assert predict.history_eth == [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0]
    assert round(predict.btc_influence, 5) == 1.0

def test_current_handler(predict, mock_ex_rates):
    predict.requester_btc = mock_ex_rates
    predict.requester_eth = mock_ex_rates
    predict.current_handler()
    assert predict.last_eth_price == 5.0
