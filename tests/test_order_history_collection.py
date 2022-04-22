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
