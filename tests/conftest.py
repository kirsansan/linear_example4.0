import pytest
from src.ethtracker.eth_tracker import Prediction
from src.ethtracker.myexeption import ConnectionLostError

p = Prediction()
p.floating_tail = [{"time": 100, "value": 1}, {"time": 500, "value": 5}]


class MockExchangeRates:
    def get_last_rates(self):
        return 10.0

    def get_current_rates_ccxt(self):
        return 5.0

    def get_historical_rates(self, param1=0, param2=1, param3=0):
        if param1 == "0":
            return [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.0]
        else:
            return [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0]


class MockExchangeRatesException:
    def get_last_rates(self):
        raise ConnectionLostError("OUGH")

    def get_historical_rates(self, param1, param2, param3):
        raise ConnectionLostError("UWEEE")


# mock_prediction = Prediction()
# mock_prediction.requester_btc = MockExchangeRates()
# mock_prediction.requester_eth = MockExchangeRates()

mock_exchange_rates = MockExchangeRates()

# def mock_func_with_exception():
#     raise ConnectionLostError("I have never lied to you")
#
#
# @pytest.fixture
# def except_me():
#     return mock_func_with_exception()


@pytest.fixture
def predict():
    return p


@pytest.fixture
def mock_ex_rates():
    return MockExchangeRates()


@pytest.fixture
def mock_ex_rates_exception():
    return MockExchangeRatesException()
