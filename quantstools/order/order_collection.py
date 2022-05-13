"""A module to store collection of orders data
"""

from numpy import isin
from .order import Order
from .price import Price
from .amount import Amount
from .symbol import Symbol

class OrderCollection:

    """Class to model collection of Order data.

    All Order objects in the collection have a same Symbol.

    Attributes
    ----------
    symbol : Symbol
        `symbol` attribute is a propety that determines the symbol for which
        collection of orders is in need.

    orders : list
        `orders` attribute is list of Order objects.
        The `orders` attribute is a readonly property.

    
    """

    def __init__(
        self,
        symbol: Symbol
        ):
        """
        Parameters
        ----------
        symbol : Symbol
            The `symbol` parameter determines the Symbol for which we want
            to have collection of Order objects.

        """
        self._orders = []
        self.symbol = symbol

    @property
    def symbol(self) -> Symbol:
        """Returns the symbol property attribute.
        
        Returns
        -------

        self._symbol : Symbol

        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: Symbol) -> None:
        """Setter for symbol property

        Parameters
        ----------
        symbol : Symbol
            The Symbol object to set as the symbol of the OrderCollection.

        Returns
        -------
        None

        """
        if not isinstance(symbol, Symbol):
            raise TypeError(
                "Expected symbol of type 'Symbol'"
                f" but got of type '{symbol.__class__.__name__}'"
            )
        self._symbol = symbol

    @property
    def orders(self) -> list:
        """Returns the orders property attribute
        """
        return self._orders

    def add_order(
        self,
        order: Order
        ):
        """Adds give order to the collection.

        Parameters
        ----------
        order : Order
            An Order object to add into the collection.
        
        Raises
        ------
        TypeError:
            Raises TypeError when the `order` parameter is not of type Order.
        ValueError:
            Raises ValueError when the `symbol` of the `order` argument is not
            same as the `self.symbol` attribute.

        Returns
        -------
        None
        """
        if not isinstance(order, Order):
            raise TypeError(
                "Expecd order of type 'Order' "
                f"but got of type '{order.__class__.__name__}'"
                )
        if not order.symbol == self.symbol:
            raise ValueError(
                f"Expected the give order's symbol to be "
                f"'{self.symbol.symbol}' "
                f"but got an order with symbol = '{order.symbol.symbol}'"
            )
        self._orders.append(order)

    def reset(self):
        """Resets the collection to initial state.
        
        Makes the collection empty of any orders and reset any other 
        settings to its initial statae.
        """
        self._orders = []

    def pop_first(self) -> Order:
        """Removes and returns the first order from the collection.
        
        Removes and returns the first order from the collection. If there 
        isn't any order in the collection, it return None.

        Returns
        -------
            : Order or None
        """
        try:
            return self._orders.pop(0)
        except IndexError:
            return None

    def pop_last(self) -> Order:
        """Removes and returns the last order from the collection.
        
        Removes and returns the last order from the collection. If there 
        isn't any order in the collection, it return None.

        Returns
        -------
            : Order or None
        """
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