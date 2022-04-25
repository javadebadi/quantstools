"""A module for order collection
"""

from .order import Order
from .price import Price
from .amount import Amount
from .symbol import Symbol

class OrderCollection:

    def __init__(
        self,
        symbol: Symbol
        ):
        self._orders = []
        self.symbol = symbol

    @property
    def orders(self) -> list:
        return self._orders

    def add_order(
        self,
        order: Order
        ):
        assert isinstance(order, Order)
        assert order.symbol == self.symbol
        self._orders.append(order)

    def reset(self):
        self._orders = []

    def remove_last_order(self) -> Order:
        try:
            return self._orders.pop()
        except IndexError:
            return None

    def get_total_value(self) -> float:
        return sum(order.get_value() for order in self._orders)

    def get_total_amount(self) -> float:
        return sum(float(order.amount.get_amount()) for order in self._orders)

    def get_avg_price(self) -> float:
        if not self._orders:
            return None
        else:
            price = self._orders[0].price
            p = self.get_total_value()/self.get_total_amount()
        return float(Price(p, price.digits, price.precision).get_price())

    def get_orders_list_of_dict(self, numeric=False) -> list:
        return [order.to_dict(numeric=numeric) for order in self._orders]

    def get_report(self):
        s = "========== Order Collection Report ==========\n"
        s += f"Number of orders = {len(self)}\n"
        s += f"Average Price = {self.get_avg_price()}\n"
        s += f"Total Value = {self.get_total_value()}\n"
        return s

    def __len__(self):
        return len(self._orders)

    def serialize(self) -> list:
        return [order.to_dict() for order in self.orders]

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if len(self.orders) != len(other.orders):
            return False
        for index, order in enumerate(self.orders):
            if other.orders[index] != order:
                return False
        return True

    def __str__(self) -> str:
        s = ""
        for order in self._orders:
            s += str(order) + "\n"
        s = s.strip()
        return s

    def __iter__(self):
        for item in self._orders:
            yield item