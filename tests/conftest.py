import pytest
from src.ethtracker.eth_tracker import Prediction
from config.config import TIME_THRESHOLD
from src.ethtracker.myexeption import ConnectionLostError

p = Prediction()
p.floating_tail = [{"time": 100, "value": 1}, {"time": 500, "value": 5}]


class MockExchangeRates:
    def get_last_rates(self):
        return 10.0

    def get_historical_rates(self, param1, param2, param3):
        return [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.0]

class MockExchangeRatesException:
    def get_last_rates(self):
        raise ConnectionLostError("OUGH")

    def get_historical_rates(self, param1, param2, param3):
        raise ConnectionLostError("UWEEE")



# mock_prediction = Prediction()
# mock_prediction.requester_btc = MockExchangeRates()
# mock_prediction.requester_eth = MockExchangeRates()

mock_exchange_rates = MockExchangeRates()

@pytest.fixture
def predict():
    return p

@pytest.fixture
def mock_ex_rates():
    return mock_exchange_rates

@pytest.fixture
def mock_ex_rates_exception():
    return MockExchangeRatesException()
