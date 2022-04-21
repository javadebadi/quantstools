import pytest
import unittest
from quantstools.price import Price
from quantstools.order import Order
from quantstools.symbol import Symbol

class TestOrder(unittest.TestCase):

    def setUp(self) -> None:
        self.symbol = Symbol('ETH-BTC')

    def test_symbol_property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), '0.05')
        assert o.symbol == self.symbol

    def test_symbol_property_raises_assertion_error(self):
        with pytest.raises(AssertionError) as exc_info:
            Order([], 'BUY', Price(0.12, 5, 4), '0.05')
        with pytest.raises(AssertionError) as exc_info:
            Order(12, 'BUY', Price(0.12, 5, 4), '0.05')

    def test_side_property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), '0.05')
        assert o.side == 'BUY'
        o = Order(self.symbol, 'SELL', Price(0.12, 5, 4), '0.05')
        assert o.side == 'SELL'

    def test_side_property_raises_assertion_error(self):
        with pytest.raises(AssertionError) as exc_info:
            Order(self.symbol, 'xyz', Price(0.12, 5, 4), '0.05')
        with pytest.raises(AssertionError) as exc_info:
            Order(self.symbol, None, Price(0.12, 5, 4), '0.05')

    def test_price_property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), '0.05')
        assert o.price == Price(0.12, 5, 4)

    def test_price_property_raises_assertion_error(self):
        with pytest.raises(AssertionError) as exc_info:
            Order(self.symbol, 'BUY', 0.12, '0.05')

    def test_amount_property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), '0.05')
        assert o.amount == '0.05'

    def test_amount_property_raises_assertion_error(self):
        with pytest.raises(AssertionError) as exc_info:
            Order(self.symbol, 'BUY', Price(0.12, 5, 4), 0.05)

    def test_type__property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), '0.05', 'LIMIT')
        assert o.type_ == 'LIMIT'
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), '0.05', 'MARKET')
        assert o.type_ == 'MARKET'

    def test_type__property_raises_assertion_error(self):
        with pytest.raises(AssertionError) as exc_info:
            Order(self.symbol, 'BUY', Price(0.12, 5, 4), 0.05, 'xyz')

    def test_to_dict(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), '0.05', 'LIMIT')
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
            amount='0.015',
            type_='LIMIT',
            )
        assert o.get_value() == pytest.approx(0.015*0.12)
        o = Order(
            symbol=self.symbol,
            side='SELL',
            price=Price(0.12, 5, 4),
            amount='0.015',
            type_='LIMIT',
            )
        assert o.get_value() == pytest.approx(-0.015*0.12)