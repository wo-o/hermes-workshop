from discount import final_price


def test_twenty_percent_discount():
    assert final_price(100, 20) == 80


def test_zero_percent_discount():
    assert final_price(100, 0) == 100


def test_full_discount():
    assert final_price(100, 100) == 0
