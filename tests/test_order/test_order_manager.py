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
    OrderManager,
)


class TestOrderManager:

    def test_generate_buy_limit_order(self):
        symbol = Symbol('BTC-USDT', 12, 6)
        m = OrderManager(symbol, 8, 4)
        o = Order(
            symbol, 'BUY', Price(40000, symbol.digits, symbol.precision), Amount(1.0, 8, 4) , 'LIMIT'
        )
        m.generate_buy_limit_order(40000, 1.0) == o

    def test_generate_buy_limit_orders_triangle(self):
        symbol = Symbol('BTC-USDT', 12, 6)
        m = OrderManager(symbol, 8, 4)
        o1 = Order(
            symbol, 'BUY', Price(40000,  symbol.digits, symbol.precision), Amount(1.0, 8, 4) , 'LIMIT'
        )
        o2 = Order(
            symbol, 'BUY', Price(40000 / (1 + 0.01 + 0.004), symbol.digits, symbol.precision), Amount(1.0 * (1 + 0.01), 8, 4) , 'LIMIT'
        )
        ocg = m.generate_buy_limit_orders_triangle(
            max_price=40000,
            min_amount=1,
            n_orders=2,
            price_decrement_rate=0.01,
            amount_increment_rate=0.01
        )
        oc = OrderCollection(symbol)
        assert oc != ocg
        oc.add_order(o1)
        assert oc != ocg
        oc.add_order(o2)
        assert oc == ocg

    def test_get_orders_history(self):
        symbol = Symbol('VRA-USDT', 10, 8)
        m = OrderManager(symbol, 12, 6)
        list_of_dict  = [
            {
                'id_': '62618deb74b0a90001a93c12',
                'symbol': 'VRA-USDT',
                'price': '0.02512359',
                'side': 'BUY',
                'amount': '7000',
                'mili_unixtime': 1650560401404,
                'is_cancelled': False,
                'is_active': False,
                'type_': 'LIMIT'
            },
            {
                'id_': 'ab5e8deb74b0a90001a93c12',
                'symbol': 'VRA-USDT',
                'price': '0.02512359',
                'side': 'SELL',
                'amount': '3500',
                'mili_unixtime': 1650560491404,
                'is_cancelled': False,
                'is_active': True,
                'type_': 'LIMIT'
            },
            ]
        m.get_orders_history(
            list_of_dict
        )
        assert len(m.ohc.done_orders) == 1
        assert len(m.ohc.active_orders) == 1
