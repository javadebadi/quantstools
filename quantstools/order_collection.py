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

    def __str__(self) -> str:
        s = ""
        for order in self._orders:
            s += str(order) + "\n"
        s = s.strip()
        return s