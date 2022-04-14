import pytest
import unittest
from quantstools.price import Price


class TestPrice:

    def test_number_property(self):
        with pytest.raises(TypeError) as excinfo:
            Price('0.00181425', 9, 8)
            assert f"Expected number of type int or float but got type 'str'" in str(excinfo)

    def test_number_property2(self):
        with pytest.raises(AssertionError) as excinfo:
            Price(125.00181425, 9, 8)
            assert f"The number of integer part '125' ould not be bigger than 1" in str(excinfo)

    def test_digits_property(self):
        with pytest.raises(TypeError) as excinfo:
            Price(0.00181425, 9.5, 8)
            assert f"Expected digits of type int but got type 'float'" in str(excinfo)

    def test_precision_property(self):
        with pytest.raises(TypeError) as excinfo:
            Price(0.00181425, 9, 8.5)
            assert f"Expected precision of type int but got type 'float'" in str(excinfo)

    def test_get_price(self):
        assert Price(0.00102030, 9, 8).get_price() == '0.00102030'
        assert Price(0.001, 9, 8).get_price() == '0.00100000'
        assert Price(6500.15, 6, 2).get_price() == '6500.15'
        assert Price(6500, 12, 8).get_price() == '6500.00000000'
        assert Price(6500, 15, 8).get_price() == '6500.00000000'

    def test_increase(self):
        assert Price(1, 3, 2).increase(percentage=0.01, fee=0) == Price(1.01, 3, 2)
        assert Price(1, 4, 3).increase(percentage=0.01, fee=0.001) == Price(1.011, 4, 3)
        assert Price(1, 4, 3).increase(percentage=0, fee=0.001) == Price(1.001, 4, 3)

    def test_decrease(self):
        assert Price(1.01, 3, 2).decrease(percentage=0.01, fee=0) == Price(1, 3, 2)
        assert Price(1.011, 4, 3).decrease(percentage=0.01, fee=0.001) == Price(1, 4, 3)
        assert Price(1.001, 4, 3).decrease(percentage=0, fee=0.001) == Price(1, 4, 3)




