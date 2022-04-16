import pytest
import unittest
from quantstools.price import Price
from quantstools.order import Order

class TestOrder:

    def test_symbol_property(self):
        o = Order('ETH-BTC', 'BUY', Price(0.12, 5, 4))
        assert o.symbol == 'ETH-BTC'

    def test_symbol_property_raises_assertion_error(self):
        with pytest.raises(AssertionError) as exc_info:
            Order([], 'BUY', Price(0.12, 5, 4))
        with pytest.raises(AssertionError) as exc_info:
            Order(12, 'BUY', Price(0.12, 5, 4))

    def test_side_property(self):
        o = Order('ETH-BTC', 'BUY', Price(0.12, 5, 4))
        assert o.side == 'BUY'
        o = Order('ETH-BTC', 'SELL', Price(0.12, 5, 4))
        assert o.side == 'SELL'

    def test_side_property_raises_assertion_error(self):
        with pytest.raises(AssertionError) as exc_info:
            Order('ETH-BTC', 'xyz', Price(0.12, 5, 4))
        with pytest.raises(AssertionError) as exc_info:
            Order('ETH-BTC', None, Price(0.12, 5, 4))

    def test_to_dict(self):
        o = Order('ETH-BTC', 'BUY', Price(0.12, 5, 4))
        assert o.to_dict() == {'side': 'BUY', 'symbol': 'ETH-BTC', 'price': '0.1200'}