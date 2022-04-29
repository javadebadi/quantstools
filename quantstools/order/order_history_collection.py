"""A module for order collection
"""
import os
import json
import logging
from typing import OrderedDict
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

    def __len__(self):
        return len(self._active_orders) + len(self._done_orders) + len(self._cancelled_orders)

    def __iter__(self):
        for order in self._active_orders.union(self._done_orders):
            yield order

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

    def __add__(self, other):
        assert isinstance(other, OrderHistoryCollection)
        assert self.symbol.symbol == other.symbol.symbol
        oc = OrderHistoryCollection(symbol=self.symbol)
        oc._active_orders = self._active_orders.union(other._active_orders)
        oc._done_orders = self._done_orders.union(other._done_orders)
        oc._cancelled_orders = self._cancelled_orders.union(other._cancelled_orders)
        return oc

    def to_json(self, filepath='order_history_collection.json'):
        with open(filepath, 'w') as f:
            json.dump(self.serialize(), f)

    def to_text(self, filepath='order_history_collection.txt'):
        with open(filepath, 'w') as f:
            f.write(str(self))


    def get_report(self):
        s = " ==================== SUMMARY ====================\n"
        s += "Order Status".ljust(20) + " | " + "#".ljust(6) + "\n"
        s += "Done Orders".ljust(20) + " | " + f"{len(self._done_orders)}".ljust(6) + "\n"
        s += "Active Orders".ljust(20) + " | " + f"{len(self._active_orders)}".ljust(6) + "\n"
        s += "Cancelled Orders".ljust(20) + " | " + f"{len(self._cancelled_orders)}".ljust(6) + "\n"
        s += "     -------------------------     \n"
        s += f"Total Amount = {self.get_total_amount()}\n" 
        s += f"Total Value = {self.get_total_value()}\n" 
        s += f"Average Price = {self.get_avg_price()}\n"
        return s

    def load_json(self, filepath='order_history_collection.json'):
        logging.info("Checking to see whether json file exists")
        if os.path.exists(filepath):
            logging.info(f"reading json file: {filepath}")
            with open(filepath, 'r') as f:
                logging.info(f"Opened the json file to read")
                serialized_data = json.load(f)
            oc = self.deserialize(serialized_data=serialized_data, inplace=False)
            self = self.__add__(oc)
            return self
        else:
            logging.warning(f"josn filepath = '{filepath}', does not exists")

    def __str__(self) -> str:
        s = "=============== ORDER HISTORY COLLECTION ===============\n"
        s += "--------------- Done Orders ---------------\n"
        for o in self.done_orders:
            s += str(o) + "\n"
        s += "--------------- Active Orders ---------------\n"
        for o in self.active_orders:
            s += str(o) + "\n"
        s += "--------------- Cancelled Orders ---------------\n"
        for o in self.cancelled_orders:
            s += str(o) + "\n"
        s += self.get_report()
        return s