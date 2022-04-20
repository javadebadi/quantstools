import pytest
import unittest
from quantstools.price import Price
from quantstools.order import Order
from quantstools.order_collection import OrderCollection

class TestOrderCollection:

    def test_add_order(self) -> None:
        oc = OrderCollection('ETH-BTC')
        o = Order('ETH-BTC', 'BUY', Price(0.015, 5, 4) , '0.15', 'LIMIT')
        oc.add_order(o)
        assert len(oc._orders) == 1
        assert oc.orders[0] == o
        o = Order('ETH-BTC', 'SELL', Price(0.016, 5, 4) , '0.5', 'LIMIT')
        oc.add_order(o)
        assert len(oc._orders) == 2
        assert oc.orders[1] == o

    def test_add_order_raises_assertion_error(self):
        oc = OrderCollection('ETH-BTC')
        o = Order('BTC-USDT', 'BUY', Price(0.015, 5, 4) , '0.15', 'LIMIT')
        with pytest.raises(AssertionError) as exc_info:
            oc.add_order(Order)
        with pytest.raises(AssertionError) as exc_info:
            oc.add_order(12)

    def test_reset(self):
        oc = OrderCollection('ETH-BTC')
        o = Order('ETH-BTC', 'BUY', Price(0.015, 5, 4) , '0.15', 'LIMIT')
        oc.add_order(o)
        assert len(oc._orders) == 1
        oc.reset()
        assert len(oc._orders) == 0

    def test_remove_last_order(self) -> None:
        oc = OrderCollection('ETH-BTC')
        o = Order('ETH-BTC', 'BUY', Price(0.015, 5, 4) , '0.15', 'LIMIT')
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
        self.oc = OrderCollection('BTC-USDT')
        o1 = Order('BTC-USDT', 'BUY', Price(40000,8,2), '1.0')
        o2 = Order('BTC-USDT', 'BUY', Price(20000,8,2), '1.0')
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
        print(self.oc.get_orders_list_of_dict()[0].values())
        assert self.oc.get_orders_list_of_dict() == l