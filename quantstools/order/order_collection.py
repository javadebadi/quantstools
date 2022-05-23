"""A module to store collection of orders data
"""

from numpy import isin
from .order import Order
from .price import Price
from .amount import Amount
from .symbol import Symbol
from typing import List

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
        ) -> None:
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

    def reset(self) -> None:
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

    def get_total_value(self, signed: bool = True) -> float:
        """Returns the sum of value of all orders in the collection.

        The total value is negative when the total value of selled stocks
        is bigger than total value of buyed stockes. Roughly it means the 
        amount of money spent is less than the amount of gained money.

        The positive total value means the amount of money spent is bigger
        than the amount of money that is gained.

        positve total value <-> SPENT > GAINED
        negative total value <-> SPENT < GAINED

        The method uses Python's sum method to sum result of .get_value()
        method of order objects insided the collection.

        Parameters
        ----------
        signed : bool
            The signed argument must always be True.

        Raises
        ------
        AssertionError
            if the `signed` parameter is not True raises AssertionError

        """
        assert signed is True
        return sum(order.get_value(signed=signed) for order in self._orders)

    def get_total_gain(self) -> float:
        """Returns net gain (net money) from collection.

        This values is just the same as tota_value multiplied by -1.
        Returns
        -------
            : float
            net gain from all orders

        """
        return -1 * self.get_total_value()

    def get_total_amount(self) -> float:
        """Returns the total amount of orders.

        It returns the total signed amount of the orders. It means that if
        sum of SELL amounts is bigger than sum of BUY amounts then this 
        method will return a negative number.

        Returns
        -------
            : float 
        """
        return sum(order.get_numeric_amount(signed=True) for order in self._orders)

    def get_avg_price(self) -> float:
        """Returns average price of orders in collection.
        
        The method calculates the average price of the orders in collection
        weighted by the amount of each order.


        Returns
        -------
            : float
            Average price of orders. If the collection is empty returns None.
            In addition, if the total amounts is 0 again the average price of
            None will be returned.
        
        """
        if not self._orders:
            return None
        total_amounts = self.get_total_amount()
        if total_amounts == 0:
            return None
        else:
            p = self.get_total_value() / total_amounts
        return Price(
            p,
            self.symbol.digits,
            self.symbol.precision,
            ).get_numeric_price()

    def get_orders_list_of_dict(self, numeric=False) -> List[dict]:
        """Returns list of orders dictionaries

        The method loops over collection items and returns a list where each
        item is a dictionary which is produced using the Order.to_dict() method of
        corresponding order object.

        Parameters
        ----------
        numeric : bool
            Default value is False.
            The argument is passed to Order.to_dict() `numeric` parameter as
            argument.

        Returns
        -------
            : List[dict]
            Returns list of dictionaries of all orders in the collection.

        """
        return [order.to_dict(numeric=numeric) for order in self._orders]

    def get_report(self) -> str:
        """Returns a report of the collection.

        It returns a summary of the collection status.


        Returns
        -------
        s : str
            String denoting the status of the collection as a report.

        """
        s = "========== Order Collection Report ==========\n"
        s += f"# of orders   = {len(self)}\n"
        s += f"Average Price = {self.get_avg_price()}\n"
        s += f"Total Value   = {self.get_total_value()}\n"
        s += f"Total Gain    = {self.get_total_gain()}\n"
        return s

    def __len__(self) -> int:
        """Returns number of orders in the collection


        Returns
        -------
            : int
            Number of order objects in the collection.

        """
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