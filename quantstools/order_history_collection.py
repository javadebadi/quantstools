"""A module for order collection
"""

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

    def clean(self):
        """Removes cancelled orders"""
        self._cancelled_orders = set()