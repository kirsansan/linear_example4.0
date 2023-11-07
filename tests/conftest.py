import pytest
from src.ethtracker.eth_tracker import Prediction
from config.config import TIME_THRESHOLD

p = Prediction()
p.floating_tail = [{"time": 100, "value": 1}, {"time": 500, "value": 5}]

@pytest.fixture
def predict():
    return p
