import unittest
import pytest
from quantstools.order_history import OrderHistory
from quantstools.price import Price
from quantstools.amount import Amount
from quantstools.order_history_collection import OrderHistoryCollection
from quantstools.symbol import Symbol

class TestOrderHistoryCollection:

    def test_init(self):
        o = OrderHistoryCollection(symbol=Symbol('BTC-USDT'))
        assert o.symbol == Symbol('BTC-USDT')
        assert o.active_orders == set()
        assert o.done_orders == set()
        assert o.cancelled_orders == set()

    def test_add_order_history_when_order_is_active(self):
        order = OrderHistory(
            id_='A4fe4f896wwefbqwe5ef6we',
            symbol=Symbol('BTC-USDT'),
            side='BUY',
            price=Price(40000, 8, 2),
            amount=Amount(1.0, 2, 1),
            mili_unixtime=15489161,
            is_active=True,
            is_cancelled=False,
            type_='LIMIT',   
        )
        oc = OrderHistoryCollection(symbol=Symbol('BTC-USDT'))
        oc.add_order_history(
            order=order
        )
        assert oc.active_orders == set([order])
        assert oc.done_orders == set()
        assert oc.cancelled_orders == set()
    
    def test_add_order_history_when_order_is_done(self):
        order = OrderHistory(
            id_='A4fe4f896wwefbqwe5ef6we',
            symbol=Symbol('BTC-USDT'),
            side='BUY',
            price=Price(40000, 8, 2),
            amount=Amount(1.0, 2, 1),
            mili_unixtime=15489161,
            is_active=False,
            is_cancelled=False,
            type_='LIMIT',   
        )
        oc = OrderHistoryCollection(symbol=Symbol('BTC-USDT'))
        oc.add_order_history(
            order=order
        )
        assert oc.active_orders == set()
        assert oc.done_orders == set([order])
        assert oc.cancelled_orders == set()
    
    def test_add_order_history_when_order_is_cancelled(self):
        order = OrderHistory(
            id_='A4fe4f896wwefbqwe5ef6we',
            symbol=Symbol('BTC-USDT'),
            side='BUY',
            price=Price(40000, 8, 2),
            amount=Amount(1.0, 2, 1),
            mili_unixtime=15489161,
            is_active=False,
            is_cancelled=True,
            type_='LIMIT',   
        )
        oc = OrderHistoryCollection(symbol=Symbol('BTC-USDT'))
        oc.add_order_history(
            order=order
        )
        assert oc.active_orders == set()
        assert oc.done_orders == set()
        assert oc.cancelled_orders == set([order])

    def test_add_order_history_when_same_order_is_added_again_after_it_is_cancelled_will_remove_from_active_orders(self):
        order = OrderHistory(
            id_='A4fe4f896wwefbqwe5ef6we',
            symbol=Symbol('BTC-USDT'),
            side='BUY',
            price=Price(40000, 8, 2),
            amount=Amount(1.0, 2, 1),
            mili_unixtime=15489161,
            is_active=True,
            is_cancelled=False,
            type_='LIMIT',   
        )
        oc = OrderHistoryCollection(symbol=Symbol('BTC-USDT'))
        oc.add_order_history(
            order=order
        )
        assert oc.active_orders == set([order])
        assert oc.done_orders == set()
        assert oc.cancelled_orders == set()
        order.cancel()
        oc.add_order_history(
            order=order
        )
        assert oc.active_orders == set()
        assert oc.done_orders == set()
        assert oc.cancelled_orders == set([order])


class TestCaseOrderHistoryCollection(unittest.TestCase):

    def setUp(self) -> None:
        self.symbol = Symbol('BTC-USDT')
        self.ohc = OrderHistoryCollection(self.symbol)
        self.ohc.add_order_history(
            OrderHistory(
                id_='1000',
                symbol=self.symbol,
                side='BUY',
                price=Price(20000, 12, 4),
                amount=Amount(1.0, 12, 6),
                mili_unixtime=100000000,
                is_active=False,
                is_cancelled=False,
                type_='LIMIT',
            )
        )
        self.ohc.add_order_history(
            OrderHistory(
                id_='2000',
                symbol=self.symbol,
                side='BUY',
                price=Price(40000, 12, 4),
                amount=Amount(1.0, 12, 6),
                mili_unixtime=200000000,
                is_active=False,
                is_cancelled=False,
                type_='LIMIT',
            )
        )

    def test_get_total_value(self):
        assert self.ohc.get_total_value(mili_unixtime__lte=1000) == pytest.approx(0)
        assert self.ohc.get_total_value(mili_unixtime__lte=100000005) == pytest.approx(20000)
        assert self.ohc.get_total_value(mili_unixtime__lte=200000005) == pytest.approx(60000)
        assert self.ohc.get_total_value() == pytest.approx(60000)

    def test_get_total_amount(self):
        assert self.ohc.get_total_amount(mili_unixtime__lte=1000) == pytest.approx(0)
        assert self.ohc.get_total_amount(mili_unixtime__lte=100000005) == pytest.approx(1)
        assert self.ohc.get_total_amount(mili_unixtime__lte=200000005) == pytest.approx(2)
        assert self.ohc.get_total_amount() == pytest.approx(2)

    def test_get_avg_price(self):
        assert self.ohc.get_avg_price(mili_unixtime_lte=1000) == pytest.approx(0)
        assert self.ohc.get_avg_price(mili_unixtime_lte=100000005) == pytest.approx(20000)
        assert self.ohc.get_avg_price(mili_unixtime_lte=200000005) == pytest.approx(30000)
        assert self.ohc.get_avg_price() == pytest.approx(30000)

    def test_get_total_profit(self):
        assert self.ohc.get_total_profit(mili_unixtime_lte=1000) == pytest.approx(0)
        with pytest.raises(ValueError) as exc_info:
            assert self.ohc.get_total_profit(mili_unixtime_lte=100000005)
        assert self.ohc.get_total_profit(
            sell_price=20000.0,
            mili_unixtime_lte=100000005
            ) == pytest.approx(0)
        assert self.ohc.get_total_profit(
            sell_price=60000.0,
            mili_unixtime_lte=100000005
            ) == pytest.approx(40000)
        assert self.ohc.get_total_profit(
            sell_price=30000.0,
            mili_unixtime_lte=200000005
            ) == pytest.approx(0)
        assert self.ohc.get_total_profit(
            sell_price=60000.0,
            mili_unixtime_lte=200000005
            ) == pytest.approx(60000)
