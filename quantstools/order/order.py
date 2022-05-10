"""A module to manage orders
"""

from .price import Price
from .amount import Amount
from .symbol import Symbol

class Order:

    """Class to represent Order objects.

    The Order objects have the following attributes:

    Attributes
    ----------
    symbol : Symbol
        The symbol for which Order object is created.
    side : str
        `side` attribute determines whether the order is a sell order or 
        a buy order.
    price : Price
        `price` attribute is a Price object which determines the price
        of order with exact given precision and number of digits
    amount : Amount
        `amount` attribte is a Amount object which determines the amount
        of order or size of the order. It determines the number of quantity
        which we want to sell or buy. Similar to `price` it has the exact
        precision and digits of the amount.
    type_ : str
        `type_` attribute determines the type of the order. It can be a limit
        order or market order.

    Example
    -------
    >>> symbol = Symbol('BTC-USDT', 12, 6, 12, 6)
    >>> price = Price(40000.0, symbl.digits, symbol.precision)
    >>> amount = Amount(1.0, symbl.amount_digits, symbol.amount_precision)
    >>> order = Order(
        symbol=symbol,
        price=price,
        amount=amount,
        side='BUY',
        type_='LIMIT',
        )

    """

    def __init__(
        self,
        symbol: Symbol,
        side: str,
        price: Price,
        amount: Amount,
        type_: str = 'LIMIT',
        ):
        self.symbol = symbol
        self.side = side
        self.price = price
        self.amount = amount
        self.type_ = type_


    @property
    def symbol(self) -> Symbol:
        """Returns the symbol property attribute.
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: Symbol) -> None:
        """Setter property for symbol attribute.

        Parameters
        ----------
        symbol : Symbol

        Returns
        -------
        None

        Raises
        ------
        TypeError
            if type of the `symbol` parameter is not Symbol a TypeError
            will be raised.
        
        """
        if not isinstance(symbol, Symbol):
            raise TypeError(
                "Expected symbol of type 'Symbol' "
                f"but got of type '{symbol.__class__.__name__}'"
                )
        self._symbol = symbol

    @property
    def side(self) -> str:
        """Returns the side property attribute
        """
        return self._side

    @side.setter
    def side(self, side: str) -> None:
        """Setter for side property attribute

        Parameters
        ----------
        side : str
            The parameter to set for side property. It must be either 'SELL'
            or 'BUY'

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Raises ValueError when the `side` is not 'BUY' or 'SELL'
        """
        if side not in ['BUY', 'SELL']:
            raise ValueError(
                "The side attribute must be either 'SELL' or 'BUY' "
                f"but got the value '{side}'"
                )
        self._side = side

    @property
    def price(self) -> Price:
        """Returns the price property attribute
        """
        return self._price

    @price.setter
    def price(self, price: Price) -> None:
        """Setter for price property attribute

        Parameters
        ----------
        price : Price
            The parameter to set as the price attribute. It must be a Price
            object.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            Raises TypeError when the `price` parameter is not a Price object.

        """
        if not isinstance(price, Price):
            raise TypeError(
                "Expected price of type 'Price' "
                f"but got of type '{price.__class__.__name__}'"
                )
        self._price = price

    @property
    def amount(self) -> Amount:
        """Returns the amount property attribute
        """
        return self._amount

    @amount.setter
    def amount(self, amount: Amount) -> None:
        """Setter for amount property attribute

        Parameters
        ----------
        amount : Amount
            The parameter to set as the amount attribute. It must be an Amount
            object.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            Raises TypeError when the `amount` parameter is not an Amount
            object.

        """
        if not isinstance(amount, Amount):
            raise TypeError(
                "Expected amount of type 'Amount' "
                f"but got of type '{amount.__class__.__name__}'"
                )
        self._amount = amount

    @property
    def type_(self) -> str:
        """Returns the type_ property attribute
        """
        return self._type_

    @type_.setter
    def type_(self, type_: str) -> None:
        """Setter for type_ property attribute

        Parameters
        ----------
        type_ : str
            The parameter to set for type_ property. It must be either 'LIMIT'
            or 'MARKET'

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Raises ValueError when the `side` is not 'LIMIT' or 'MARKET'
        """
        if type_ not in ['LIMIT', 'MARKET']:
            raise ValueError(
                "The type_ attribute must be either 'LIMIT' or 'MARKET' "
                f"but got the value '{type_}'"
                )
        self._type_ = type_

    def get_price(self, numeric=False) -> Price:
        if numeric is False:
            return self.price.get_price()
        else:
            return float(self.get_price())

    def get_amount(self, numeric=False):
        if numeric is False:
            return self.amount.get_amount()
        else:
            return self.get_numeric_amount()

    def get_numeric_amount(self) -> float:
        if self.side == 'BUY':
            return abs(float(self.amount.get_number()))
        elif self.side == 'SELL':
            return - abs(float(self.amount.get_number()))

    def get_value(self, rounding=4) -> float:
        return round(self.get_numeric_amount() * float(self.get_price()), rounding)

    def to_dict(self, numeric=False) -> dict:
        d = {}
        d['symbol'] = self.symbol.symbol
        d['side'] = self.side
        d['price'] = self.get_price()
        d['amount'] = self.amount.get_amount()
        if numeric is True:
            d['price'] = float(d['price'])
            d['amount'] = float(d['amount'])
        d['type_'] = self.type_
        return d

    def serialize(self, keys=['symbol', 'side', 'amount', 'price']) -> dict:
        d = self.to_dict(numeric=False)
        return dict((k, d[k]) for k in keys if k in d)

    def __eq__(self, other) -> bool:
        if self.to_dict() == other.to_dict():
            return True
        else:
            return False

    def __str__(self) -> str:
        return f'{self.amount.get_amount()} | {self.get_price()} | {self.get_value()}'


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)