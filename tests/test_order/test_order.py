import pytest
import unittest
from quantstools.order import (
    Price,
    Amount,
    Order,
    Symbol,
)

class TestOrder(unittest.TestCase):

    def setUp(self) -> None:
        self.symbol = Symbol('ETH-BTC', 12, 4)

    def test_symbol_property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2))
        assert o.symbol == self.symbol

    def test_symbol_property_raises_assertion_error(self):
        with pytest.raises(AssertionError) as exc_info:
            Order([], 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2))
        with pytest.raises(AssertionError) as exc_info:
            Order(12, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2))

    def test_side_property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2))
        assert o.side == 'BUY'
        o = Order(self.symbol, 'SELL', Price(0.12, 5, 4), Amount(0.05, 4,2))
        assert o.side == 'SELL'

    def test_side_property_raises_assertion_error(self):
        with pytest.raises(AssertionError) as exc_info:
            Order(self.symbol, 'xyz', Price(0.12, 5, 4), Amount(0.05, 4,2))
        with pytest.raises(AssertionError) as exc_info:
            Order(self.symbol, None, Price(0.12, 5, 4), Amount(0.05, 4,2))

    def test_price_property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2))
        assert o.price == Price(0.12, 5, 4)

    def test_price_property_raises_assertion_error(self):
        with pytest.raises(AssertionError) as exc_info:
            Order(self.symbol, 'BUY', 0.12, '0.05')

    def test_amount_property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2))
        assert o.amount == Amount(0.05, 4,2)

    def test_amount_property_raises_assertion_error(self):
        with pytest.raises(AssertionError) as exc_info:
            Order(self.symbol, 'BUY', Price(0.12, 5, 4), 0.05)

    def test_type__property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2), 'LIMIT')
        assert o.type_ == 'LIMIT'
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2), 'MARKET')
        assert o.type_ == 'MARKET'

    def test_type__property_raises_assertion_error(self):
        with pytest.raises(AssertionError) as exc_info:
            Order(self.symbol, 'BUY', Price(0.12, 5, 4), 0.05, 'xyz')

    def test_to_dict(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2), 'LIMIT')
        assert o.to_dict() == {
            'side': 'BUY',
            'symbol': 'ETH-BTC',
            'price': '0.1200',
            'amount': '0.05',
            'type_': 'LIMIT',
            }
        assert o.to_dict(numeric=True) == {
            'side': 'BUY',
            'symbol': 'ETH-BTC',
            'price': 0.12,
            'amount': 0.05,
            'type_': 'LIMIT',
            }

    def test_get_value(self):
        o = Order(
            symbol=self.symbol,
            side='BUY',
            price=Price(0.12, 5, 4),
            amount=Amount(0.015, 4,3),
            type_='LIMIT',
            )
        assert o.get_value() == pytest.approx(0.015*0.12)
        o = Order(
            symbol=self.symbol,
            side='SELL',
            price=Price(0.12, 5, 4),
            amount=Amount(0.015, 4,3),
            type_='LIMIT',
            )
        assert o.get_value() == pytest.approx(-0.015*0.12)