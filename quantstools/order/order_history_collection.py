"""A module for order collection
"""

from quantstools.order.amount import Amount
from .order import Order
from .order_history import OrderHistory
from .order_collection import OrderCollection
from .price import Price
from .symbol import Symbol

class OrderHistoryCollection:

    def __init__(
        self,
        symbol: Symbol
        ) -> None:
        self._symbol = symbol
        self._active_orders = set()
        self._done_orders = set()
        self._cancelled_orders = set()

    @property
    def symbol(self) -> Symbol:
        return self._symbol

    @property
    def active_orders(self) -> set:
        return self._active_orders

    @property
    def done_orders(self) -> set:
        return self._done_orders

    @property
    def cancelled_orders(self) -> set:
        return self._cancelled_orders

    def _add_order_history(self, order):
        assert isinstance(order, OrderHistory)
        if order.is_active:
            self.active_orders.add(order)
        else:
            self.active_orders.discard(order)
            if order.is_cancelled:
                self.cancelled_orders.add(order)
            else:
                self.done_orders.add(order)

    def add_order_history(self, order):
        if isinstance(order, OrderHistory):
            self._add_order_history(order)
        else:
            # if it is not OrderHistory
            # it must be iterable of OrderHistory objects
            for order_ in set(order):
                self._add_order_history(order_)

    def filter_by_mili_unixtime(self, mili_unixtime__lte=None):
        if mili_unixtime__lte is None:
            return self
        else:
            new_ohc = OrderHistoryCollection(self.symbol)
            for order in self.done_orders:
                if order.mili_unixtime <= mili_unixtime__lte:
                    new_ohc.add_order_history(order)
            for order in self.active_orders:
                if order.mili_unixtime <= mili_unixtime__lte:
                    new_ohc.add_order_history(order)
            for order in self.cancelled_orders:
                if order.mili_unixtime <= mili_unixtime__lte:
                    new_ohc.add_order_history(order)
            return new_ohc

    def get_total_value(self, mili_unixtime__lte=None):
        if mili_unixtime__lte is None:
            return sum(order.get_value() for order in self._done_orders)
        else:
            return self.filter_by_mili_unixtime(mili_unixtime__lte=mili_unixtime__lte).get_total_value(mili_unixtime__lte=None)

    def get_total_amount(self, mili_unixtime__lte=None):
        if mili_unixtime__lte is None:
            return sum(order.get_amount(numeric=True) for order in self._done_orders)
        else:
            return self.filter_by_mili_unixtime(mili_unixtime__lte=mili_unixtime__lte).get_total_amount(mili_unixtime__lte=None)

    def get_avg_price(self, mili_unixtime_lte=None) -> float:
        total_value = self.get_total_value(mili_unixtime__lte=mili_unixtime_lte)
        total_amount = self.get_total_amount(mili_unixtime__lte=mili_unixtime_lte)
        if total_amount == 0:
            return 0
        return total_value / total_amount

    def get_total_profit(self, sell_price: float = None, mili_unixtime_lte: int = None):
        total_value = self.get_total_value(mili_unixtime__lte=mili_unixtime_lte)
        total_amount = self.get_total_amount(mili_unixtime__lte=mili_unixtime_lte)
        if total_amount == 0.0:
            return total_value
        else:
            if sell_price is None:
                raise ValueError("Sell Price must be provided when total amount is not zero")
            return sell_price * total_amount - total_value

    def clean(self):
        """Removes cancelled orders"""
        self._cancelled_orders = set()

    def serialize(self):
        serialized_data = {}
        serialized_data["active_orders"] = [order.serialize() for order in self._active_orders]
        serialized_data["done_orders"] = [order.serialize() for order in self._done_orders]
        serialized_data["cancelled_orders"] = [order.serialize() for order in self._cancelled_orders]
        return serialized_data

    def deserialize(self, serialized_data, inplace=False):
        assert {"active_orders", "done_orders", "cancelled_orders"} == set(serialized_data.keys())
        oc = OrderHistoryCollection(self.symbol)
        o = OrderHistory(
            id_='FAKE',
            symbol=self.symbol,
            side='BUY',
            price=Price(0),
            amount=Amount(0),
            mili_unixtime=0,
            )
        for order_category in ["active_orders", "done_orders", "cancelled_orders"]:
            orders_data = serialized_data[order_category]
            for data in orders_data:
                if inplace is True:
                    self.add_order_history(o.deserialize(data))
                else:
                    oc.add_order_history(o.deserialize(data))
        if inplace is True:
            return self
        else:
            return oc