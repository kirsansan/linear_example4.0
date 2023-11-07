from src.ethtracker.eth_tracker import Prediction
from config.config import TIME_THRESHOLD

def test_add_to_floating_tail(predict):
    # TIME_THRESHOLD = 200
    predict.add_to_floating_tail(TIME_THRESHOLD + 400, 6)
    assert predict.floating_tail == [{'time': 500, 'value': 4}, {'time': TIME_THRESHOLD + 400, 'value': 5}]
