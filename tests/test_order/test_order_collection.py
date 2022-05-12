import pytest
import unittest
from quantstools.order import (
    Symbol,
    Price,
    Amount,
    Order,
    OrderCollection,
)


class TestOrderCollection(unittest.TestCase):

    def setUp(self) -> None:
        self.symbol = Symbol('ETH-BTC', 5, 4, 4, 2)

    def test_order_collection___init__(self):
        symbol = Symbol('ETH-BTC', 5, 4, 4, 2)
        oc = OrderCollection(symbol)
        assert oc.symbol == symbol
        assert oc._orders == []

    def test_order_collection_symbol_property_raise_type_error(self):
        message = f"Expected symbol of type 'Symbol' but got of type 'str'"
        with pytest.raises(TypeError) as exc_info:
            oc = OrderCollection('ETH-BTC')
        assert exc_info.match(message)

    def test_add_order(self) -> None:
        oc = OrderCollection(self.symbol)
        o = Order(self.symbol, 'BUY', Price(0.015, self.symbol.digits, self.symbol.precision) , Amount(0.15, self.symbol.amount_digits, self.symbol.amount_precision), 'LIMIT')
        oc.add_order(o)
        assert len(oc._orders) == 1
        assert oc.orders[0] == o
        o = Order(self.symbol, 'SELL', Price(0.016, self.symbol.digits, self.symbol.precision) , Amount(0.15, self.symbol.amount_digits, self.symbol.amount_precision), 'LIMIT')
        oc.add_order(o)
        assert len(oc._orders) == 2
        assert oc.orders[1] == o

    def test_add_order_raises_assertion_error(self):
        oc = OrderCollection(self.symbol)
        o = Order(Symbol('BTC-USDT', 12, 4, 12, 6), 'BUY', Price(0.015, self.symbol.digits, self.symbol.precision) , Amount(0.15, self.symbol.amount_digits, self.symbol.amount_precision), 'LIMIT')
        with pytest.raises(AssertionError) as exc_info:
            oc.add_order(Order)
        with pytest.raises(AssertionError) as exc_info:
            oc.add_order(12)

    def test_reset(self):
        oc = OrderCollection(self.symbol)
        o = Order(self.symbol, 'BUY', Price(0.015, self.symbol.digits, self.symbol.precision) , Amount(0.15, self.symbol.amount_digits, self.symbol.amount_precision), 'LIMIT')
        oc.add_order(o)
        assert len(oc._orders) == 1
        oc.reset()
        assert len(oc._orders) == 0

    def test_remove_last_order(self) -> None:
        oc = OrderCollection(self.symbol)
        o = Order(self.symbol, 'BUY', Price(0.015, self.symbol.digits, self.symbol.precision) , Amount(0.15, self.symbol.amount_digits, self.symbol.amount_precision), 'LIMIT')
        oc.add_order(o)
        assert len(oc._orders) == 1
        assert oc.orders[0] == o
        order = oc.remove_last_order()
        assert order == o
        assert len(oc._orders) == 0
        order = oc.remove_last_order()
        assert order is None


class TestCaseOrderCollection(unittest.TestCase):

    def setUp(self) -> None:
        self.symbol = Symbol('BTC-USDT', 8, 2, 3, 1)
        self.oc = OrderCollection(self.symbol)
        o1 = Order(self.symbol, 'BUY', Price(40000, self.symbol.digits, self.symbol.precision), Amount(1.0,  self.symbol.amount_digits, self.symbol.amount_precision))
        o2 = Order(self.symbol, 'BUY', Price(20000, self.symbol.digits, self.symbol.precision), Amount(1.0,  self.symbol.amount_digits, self.symbol.amount_precision))
        self.oc.add_order(o1)
        self.oc.add_order(o2)

    def test_get_total_value(self) -> None:
        assert self.oc.get_total_value() == pytest.approx(60000)

    def test_get_total_amount(self) -> None:
        assert self.oc.get_total_amount() == pytest.approx(2.0)

    def test_get_avg_price(self) -> None:
        assert self.oc.get_avg_price() == pytest.approx(60000/2)

    def test_get_orders_list_of_dict(self) -> None:
        l = [
            {'symbol': 'BTC-USDT', 'side': 'BUY', 'price': '40000.00', 'amount': '1.0', 'type_': 'LIMIT'},
            {'symbol': 'BTC-USDT', 'side': 'BUY', 'price': '20000.00', 'amount': '1.0', 'type_': 'LIMIT'},
        ]
        assert self.oc.get_orders_list_of_dict() == l

    def test_get_report(self) -> None:
        s = "========== Order Collection Report ==========\n"
        s += f"Number of orders = 2\n"
        s += f"Average Price = 30000.0\n"
        s += f"Total Value = 60000.0\n"
        assert self.oc.get_report() == s

    def test_len(self) -> None:
        assert len(self.oc) == 2

    def test_iter(self) -> None:
        for index, item in enumerate(self.oc):
            assert item == self.oc._orders[index]