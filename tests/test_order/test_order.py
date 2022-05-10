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
        self.symbol = Symbol('ETH-BTC', 12, 4, 12, 6)

    def test_symbol_property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2))
        assert o.symbol == self.symbol

    def test_symbol_property_raises_type_error(self):

        message = "Expected symbol of type 'Symbol' but got of type 'list'"
        with pytest.raises(TypeError) as exc_info:
            Order([], 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2))
        exc_info.match(message)

        message = "Expected symbol of type 'Symbol' but got of type 'int'"
        with pytest.raises(TypeError) as exc_info:
            Order(12, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2))
        exc_info.match(message)

    def test_side_property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2))
        assert o.side == 'BUY'
        o = Order(self.symbol, 'SELL', Price(0.12, 5, 4), Amount(0.05, 4,2))
        assert o.side == 'SELL'

    def test_side_property_raises_value_error(self):
        message = "The side attribute must be either 'SELL' or 'BUY' but got the value 'ok'"
        with pytest.raises(ValueError) as exc_info:
            Order(self.symbol, 'ok', Price(0.12, 5, 4), Amount(0.05, 4,2))
        exc_info.match(message)

    def test_price_property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2))
        assert o.price == Price(0.12, 5, 4)

    def test_price_property_raises_type_error(self):
        message = "Expected price of type 'Price' but got of type 'str'"
        with pytest.raises(TypeError) as exc_info:
            Order(self.symbol, 'BUY', '0.12', Amount(0.05, 4,2))
        exc_info.match(message)

    def test_amount_property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2))
        assert o.amount == Amount(0.05, 4,2)

    def test_amount_property_raises_type_error(self):
        message = "Expected amount of type 'Amount' but got of type 'str'"
        with pytest.raises(TypeError) as exc_info:
            Order(self.symbol, 'BUY', Price(0.12, 5, 4), '0.05')
        exc_info.match(message)

    def test_type__property(self):
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2), 'LIMIT')
        assert o.type_ == 'LIMIT'
        o = Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2), 'MARKET')
        assert o.type_ == 'MARKET'

    def test_type__property_raises_value_error(self):
        message = "The type_ attribute must be either 'LIMIT' or 'MARKET' but got the value 'xyz'"
        with pytest.raises(ValueError) as exc_info:
            Order(self.symbol, 'BUY', Price(0.12, 5, 4), Amount(0.05, 4,2), 'xyz')
        exc_info.match(message)



class TestOrderTestCase(unittest.TestCase):

    def setUp(self):
        self.symbol = Symbol('ETH-BTC', 12, 4, 12, 6)
        self.o = Order(self.symbol, 'SELL', Price(0.12, 12, 4), Amount(0.05, 12, 6), 'LIMIT')

    def test_get_price(self):
        assert pytest.approx(self.o.get_price()) == '0.1200'
        assert pytest.approx(self.o.get_price(numeric=True)) == 0.12

    def test_get_amount(self):
        assert pytest.approx(self.o.get_amount()) == '0.050000'
        assert pytest.approx(self.o.get_amount(numeric=True)) == 0.05

    def test_get_numeric_amount(self):
        assert pytest.approx(self.o.get_numeric_amount()) == -0.05
        assert pytest.approx(self.o.get_numeric_amount(signed=False)) == 0.05

    def test_get_value(self):
        assert pytest.approx(self.o.get_value()) == round(-0.05 * 0.12, 4)
        assert pytest.approx(self.o.get_value(signed=False)) == round(0.05 * 0.12, 4)

    def test_to_dict(self):
        assert self.o.to_dict() == {
            'symbol':'ETH-BTC',
            'amount': '0.050000',
            'price':'0.1200',
            'side': 'SELL',
            'type_': 'LIMIT',
            }

    def test_serialize(self):
        assert self.o.serialize() == {
            'symbol':'ETH-BTC',
            'amount': '0.050000',
            'price':'0.1200',
            'side': 'SELL',
            }

    def test_serialize_full_depth(self):
        assert self.o.serialize_full_depth() == {
            'symbol': {
                'symbol' : 'ETH-BTC',
                'digits' : 12,
                'precision': 4,
                'amount_digits': 12,
                'amount_precision': 6,
            },
            'amount': 0.050000,
            'price': 0.1200,
            'side': 'SELL',
            'type_': 'LIMIT',
            }

    def test_deserialize(self):
        serialized_data = {
            'symbol': {
                'symbol' : 'ETH-BTC',
                'digits' : 12,
                'precision': 4,
                'amount_digits': 12,
                'amount_precision': 6,
            },
            'amount': 0.050000,
            'price': 0.1200,
            'side': 'SELL',
            'type_': 'LIMIT',
            }
        o = Order(self.symbol, 'SELL', Price(0.12, 12, 4), Amount(0.05, 12, 6), 'LIMIT')
        assert o.deserialize(serialized_data) == self.o

    def test___eq__(self):
        assert self.o == Order(self.symbol, 'SELL', Price(0.12, 12, 4), Amount(0.05, 12, 6), 'LIMIT')
        assert self.o != Order(self.symbol, 'BUY', Price(0.12, 12, 4), Amount(0.05, 12, 6), 'LIMIT')

    def test___str__(self):
        assert str(self.o) == '| SELL|          -0.05|        0.1200|  -0.006|'