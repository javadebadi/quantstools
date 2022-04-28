import os
import json
import unittest
import pytest
from quantstools.order import (
    Symbol,
    Price,
    Amount,
    Order,
    OrderHistory,
    OrderCollection,
    OrderHistoryCollection,
)


class TestOrderHistoryCollection:

    def test_init(self):
        symbol = Symbol('BTC-USDT', 8, 2, 12, 6)
        o = OrderHistoryCollection(symbol=symbol)
        assert o.symbol == Symbol('BTC-USDT', 8, 2, 12, 6)
        assert o.active_orders == set()
        assert o.done_orders == set()
        assert o.cancelled_orders == set()

    def test_add_order_history_when_order_is_active(self):
        symbol = Symbol('BTC-USDT', 8, 2, 12, 6)
        order = OrderHistory(
            id_='A4fe4f896wwefbqwe5ef6we',
            symbol=symbol,
            side='BUY',
            price=Price(40000, symbol.digits, symbol.precision),
            amount=Amount(1.0, 2, 1),
            mili_unixtime=15489161,
            is_active=True,
            is_cancelled=False,
            type_='LIMIT',   
        )
        oc = OrderHistoryCollection(symbol=symbol)
        oc.add_order_history(
            order=order
        )
        assert oc.active_orders == set([order])
        assert oc.done_orders == set()
        assert oc.cancelled_orders == set()

    def test___add__(self):
        symbol = Symbol('BTC-USDT', 8, 2, 12, 6)
        order = OrderHistory(
            id_='A4fe4f896wwefbqwe5ef6we',
            symbol=symbol,
            side='BUY',
            price=Price(40000, symbol.digits, symbol.precision),
            amount=Amount(1.0, symbol.amount_digits, symbol.amount_precision),
            mili_unixtime=15489161,
            is_active=True,
            is_cancelled=False,
            type_='LIMIT',   
        )
        oc = OrderHistoryCollection(symbol=symbol)
        oc.add_order_history(
            order=order
        )
        orderx = OrderHistory(
            id_='Ow;9wefOif2366wefbw',
            symbol=symbol,
            side='BUY',
            price=Price(40000, symbol.digits, symbol.precision),
            amount=Amount(1.0, symbol.amount_digits, symbol.amount_precision),
            mili_unixtime=17489161,
            is_active=True,
            is_cancelled=False,
            type_='LIMIT',   
        )
        ocx = OrderHistoryCollection(symbol=symbol)
        ocx.add_order_history(
            order=orderx
        )
        assert (oc + ocx).active_orders == set([order, orderx])
        assert (oc + ocx).done_orders == set([])
        assert (oc + ocx).cancelled_orders == set([])

    
    def test_add_order_history_when_order_is_done(self):
        symbol = Symbol('BTC-USDT', 8, 2, 12, 6)
        order = OrderHistory(
            id_='A4fe4f896wwefbqwe5ef6we',
            symbol=symbol,
            side='BUY',
            price=Price(40000, symbol.digits, symbol.precision),
            amount=Amount(1.0, 2, 1),
            mili_unixtime=15489161,
            is_active=False,
            is_cancelled=False,
            type_='LIMIT',   
        )
        oc = OrderHistoryCollection(symbol=symbol)
        oc.add_order_history(
            order=order
        )
        assert oc.active_orders == set()
        assert oc.done_orders == set([order])
        assert oc.cancelled_orders == set()
    
    def test_add_order_history_when_order_is_cancelled(self):
        symbol = Symbol('BTC-USDT', 8, 2, 12, 6)
        order = OrderHistory(
            id_='A4fe4f896wwefbqwe5ef6we',
            symbol=symbol,
            side='BUY',
            price=Price(40000, symbol.digits, symbol.precision),
            amount=Amount(1.0, 2, 1),
            mili_unixtime=15489161,
            is_active=False,
            is_cancelled=True,
            type_='LIMIT',   
        )
        oc = OrderHistoryCollection(symbol=symbol)
        oc.add_order_history(
            order=order
        )
        assert oc.active_orders == set()
        assert oc.done_orders == set()
        assert oc.cancelled_orders == set([order])

    def test_add_order_history_when_same_order_is_added_again_after_it_is_cancelled_will_remove_from_active_orders(self):
        symbol = Symbol('BTC-USDT', 8, 2, 12, 6)
        order = OrderHistory(
            id_='A4fe4f896wwefbqwe5ef6we',
            symbol=symbol,
            side='BUY',
            price=Price(40000, symbol.digits, symbol.precision),
            amount=Amount(1.0, 2, 1),
            mili_unixtime=15489161,
            is_active=True,
            is_cancelled=False,
            type_='LIMIT',   
        )
        oc = OrderHistoryCollection(symbol=symbol)
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
        self.symbol = Symbol('BTC-USDT', 8, 2, 12, 6)
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


    def test_serialize(self):
        serialized = self.ohc.serialize()
        assert list(serialized.keys()) == ["active_orders", "done_orders", "cancelled_orders"]
        assert serialized["active_orders"] == []
        assert serialized["cancelled_orders"] == []
        assert len(serialized["done_orders"]) == 2
        assert set(serialized["done_orders"][0].keys()) == set(["symbol", "id_", "side", "price", "amount", "mili_unixtime", "is_active", "is_cancelled", "type_"])
        s1 = {
                    "symbol": "BTC-USDT",
                    "id_": "1000",
                    "side": "BUY",
                    "price": "20000.0000",
                    "amount": "1.000000",
                    "mili_unixtime": 100000000,
                    "is_active": False,
                    "is_cancelled": False,
                    "type_": "LIMIT",
                }
        s2 = {
                    "symbol": "BTC-USDT",
                    "id_": "2000",
                    "side": "BUY",
                    "price": "40000.0000",
                    "amount": "1.000000",
                    "mili_unixtime": 200000000,
                    "is_active": False,
                    "is_cancelled": False,
                    "type_": "LIMIT",
                }
        
        assert serialized["done_orders"][0] == s1 or serialized["done_orders"][0] == s2
        assert serialized["done_orders"][1] == s1 or serialized["done_orders"][1] == s2

    def test_deserialize(self):
        serialized_data = {}
        s1 = {
                    "symbol": "BTC-USDT",
                    "id_": "1000",
                    "side": "BUY",
                    "price": "20000.0000",
                    "amount": "1.000000",
                    "mili_unixtime": 100000000,
                    "is_active": False,
                    "is_cancelled": False,
                    "type_": "LIMIT",
                }
        s2 = {
                    "symbol": "BTC-USDT",
                    "id_": "2000",
                    "side": "BUY",
                    "price": "40000.0000",
                    "amount": "1.000000",
                    "mili_unixtime": 200000000,
                    "is_active": False,
                    "is_cancelled": False,
                    "type_": "LIMIT",
                }
        with pytest.raises(AssertionError) as exc_info:
            self.ohc.deserialize(serialized_data=serialized_data)
        serialized_data = {
            "done_orders": [
                s1,
                s2,
            ],
            "cancelled_orders": [],
            "active_orders": [],
        }
        assert self.ohc.serialize() == serialized_data


    def test_serialize_deserialize(self):
        serialized_data = self.ohc.serialize()
        oc = self.ohc.deserialize(serialized_data)
        assert oc.done_orders == self.ohc.done_orders
        assert oc.active_orders == self.ohc.active_orders
        assert oc.cancelled_orders == self.ohc.cancelled_orders

    def test_to_json(self):
        filepath = 'test_order_history_collection.json'
        self.ohc.to_json(filepath)
        assert os.path.exists(filepath)
        os.remove(filepath)
