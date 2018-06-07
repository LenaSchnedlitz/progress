"""Helper functions"""


def percentage(dividend, divisor):
    assert 0 <= dividend < divisor
    assert 0 < divisor
    return dividend / divisor * 100
