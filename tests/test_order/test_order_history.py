from datetime import datetime
import unittest
import pytz
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
from quantstools.order.exception import OrderError, OrderCancelError


class TestOrderHistory:

    def test_normal_values_for_properties(self):
        symbol = Symbol('ETH-BTC', 5, 4, 10, 6)
        o = OrderHistory(
            id_='awe6623f2366f2f2fs',
            symbol=symbol,
            side='BUY',
            price=Price(0.12, symbol.digits, symbol.precision),
            amount=Amount(0.015, 5, 3),
            mili_unixtime=1650160131557,
            is_active=True,
            is_cancelled=False,
            type_='LIMIT',
        )
        assert o.id_ == 'awe6623f2366f2f2fs'
        assert o.is_active is True
        assert o.is_cancelled is False
        assert o.mili_unixtime == 1650160131557

    def test_id__property_raises_error(self):
        symbol = Symbol('ETH-BTC', 5, 4, 10, 6)
        with pytest.raises(AssertionError) as exc_info:
            o = OrderHistory(
            id_=15,
            symbol=symbol,
            side='BUY',
            price=Price(0.12, symbol.digits, symbol.precision),
            amount=Amount(0.015, 5, 3),
            mili_unixtime=1650160131557,
            is_active=True,
            is_cancelled=False,
            type_='LIMIT',
        )

    def test_is_active_property_raises_error(self):
        symbol = Symbol('ETH-BTC', 5, 4, 10, 6)
        with pytest.raises(AssertionError) as exc_info:
            o = OrderHistory(
            id_='fweoino845fwef',
            symbol=symbol,
            side='BUY',
            price=Price(0.12, symbol.digits, symbol.precision),
            amount=Amount(0.015, 5, 3),
            mili_unixtime=1650160131557,
            is_active=98,
            is_cancelled=False,
            type_='LIMIT',
            )

    def test_is_cancelled_property_raises_error(self):
        symbol = Symbol('ETH-BTC', 5, 4, 10, 6)
        with pytest.raises(AssertionError) as exc_info:
            o = OrderHistory(
            id_='fweoino845fwef',
            symbol=symbol,
            side='BUY',
            price=Price(0.12, symbol.digits, symbol.precision),
            amount=Amount(0.015, 5, 3),
            mili_unixtime=1650160131557,
            is_active=True,
            is_cancelled='xyz',
            type_='LIMIT',
            )

    def test_mili_unixtime_property_raises_error(self):
        symbol = Symbol('ETH-BTC', 5, 4, 10, 6)
        with pytest.raises(AssertionError) as exc_info:
            o = OrderHistory(
            id_='fweoino845fwef',
            symbol=symbol,
            side='BUY',
            price=Price(0.12, symbol.digits, symbol.precision),
            amount=Amount(0.015, 5, 3),
            mili_unixtime=1650160131557.9594,
            is_active=True,
            is_cancelled=False,
            type_='LIMIT',
            )

    def test_cancel_method_make_is_cancelled_true_and_is_active_false(self):
        symbol = Symbol('ETH-BTC', 5, 4, 10, 6)
        o = OrderHistory(
            id_='fweoino845fwef',
            symbol=symbol,
            side='BUY',
            price=Price(0.12, symbol.digits, symbol.precision),
            amount=Amount(0.015, 5, 3),
            mili_unixtime=1650160131557,
            is_active=True,
            is_cancelled=False,
            type_='LIMIT',
            )
        o.cancel()
        assert o.is_active is False
        assert o.is_cancelled is True

    def test_cancel_metho_raises_error_when_is_active_is_false(self):
        symbol = Symbol('ETH-BTC', 5, 4, 10, 6)
        o = OrderHistory(
            id_='fweoino845fwef',
            symbol=symbol,
            side='BUY',
            price=Price(0.12, symbol.digits, symbol.precision),
            amount=Amount(0.015, 5, 3),
            mili_unixtime=1650160131557,
            is_active=False,
            is_cancelled=False,
            type_='LIMIT',
            )
        with pytest.raises(OrderCancelError) as exc_info:
            o.cancel()
        message = f"Non-active order with id = 'fweoino845fwef' could not be cancelled"
        assert exc_info.match(message)

    def test_deactivate(self):
        symbol = Symbol('ETH-BTC', 5, 4, 10, 6)
        o = OrderHistory(
            id_='fweoino845fwef',
            symbol=symbol,
            side='BUY',
            price=Price(0.12, symbol.digits, symbol.precision),
            amount=Amount(0.015, 5, 3),
            mili_unixtime=1650160131557,
            is_active=True,
            is_cancelled=False,
            type_='LIMIT',
            )
        assert o.is_active is True
        o.deactivate()
        assert o.is_active is False

    def test_get_value(self):
        symbol = Symbol('ETH-BTC', 5, 4, 10, 6)
        o = OrderHistory(
            id_='fweoino845fwef',
            symbol=symbol,
            side='BUY',
            price=Price(0.12, symbol.digits, symbol.precision),
            amount=Amount(0.015, 5, 3),
            mili_unixtime=1650160131557,
            is_active=True,
            is_cancelled=False,
            type_='LIMIT',
            )
        assert o.get_value() == pytest.approx(0.015*0.12)

    def test_from_order(self):
        symbol = Symbol('ETH-BTC', 5, 4, 10, 6)
        order = Order(
            symbol,
            'BUY',
            Price(0.12, symbol.digits, symbol.precision),
            Amount(0.15, 5, 2),
            'LIMIT',
        )
        o = OrderHistory.from_order(
            id_='a48ryx2wej62fx23wga3b',
            order=order,
            mili_unixtime=1594936134,
        )
        assert o.price == Price(0.12, symbol.digits, symbol.precision)
        assert o.id_ == 'a48ryx2wej62fx23wga3b'



class TestCaseOrderHistory(unittest.TestCase):

    def setUp(self) -> None:
        symbol = Symbol('ETH-BTC', 5, 4, 10, 6)
        self.o = OrderHistory(
                id_='fweoino845fwef',
                symbol=symbol,
                side='BUY',
                price=Price(0.12, symbol.digits, symbol.precision),
                amount=Amount(0.015, 5, 3),
                mili_unixtime=0,
                is_active=True,
                is_cancelled=False,
                type_='LIMIT',
                )

    def test_get_mili_unixtime(self):
        assert self.o.get_mili_unixtime() == 0

    def test_get_unixtime(self):
        assert self.o.get_unixtime() == 0

    def test_get_utcdatetime(self):
        assert datetime(1970, 1, 1, 0, 0, 0) == self.o.get_utcdatetime()

    def test_get_date_in_timezone(self):
        assert datetime(1970, 1, 1, 3, 30, 0) == self.o.get_date_in_timezone(tz='Asia/Tehran').replace(tzinfo=None)

    def test_order(self):
        symbol = Symbol('ETH-BTC', 5, 4, 10, 6)
        assert self.o.order == Order(
                symbol=symbol,
                side='BUY',
                price=Price(0.12, symbol.digits, symbol.precision),
                amount=Amount(0.015, 5, 3),
                type_='LIMIT',
                )

    def test_hash(self):
        assert hash(self.o) == hash(self.o.id_)



        