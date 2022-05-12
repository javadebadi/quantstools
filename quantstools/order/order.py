"""A module to model data for orders 
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

    def get_price(self, numeric: bool = False) -> str:
        """Returns the price of the order as string or float

        Parameters
        ----------
        numeric : bool
            Default value is False.
            Determines wheter the return result is numeric or string.

        Returns
        -------
        str or float
        """
        if numeric is False:
            return self.price.get_price()
        else:
            return self.price.get_numeric_price()

    def get_amount(self, numeric: bool = False):
        """Returns the amount of the order as string or float

        Parameters
        ----------
        numeric : bool
            Default value is False.
            Determines wheter the return result is numeric or string.

        Returns
        -------
        str or float
        """
        if numeric is False:
            return self.amount.get_amount()
        else:
            return self.amount.get_numeric_amount()


    def get_numeric_amount(self, signed: bool = True) -> float:
        """Returns the (signed) numeric amount of the order.
        
        Parameters
        ----------
        signed : bool
            Default value is True.
            Determine wheter the returned amount is signed or not. When the 
            amount is signed for SELL orders the amount is negative and for
            BUY orders it is positive. When signed is set to False, then
            always the positive value for amount will be returned.

        Returns
        -------
            : float
            signed or not-signed amount of the order
        """
        num = self.get_amount(numeric=True)
        if signed is True:
            if self.side == 'BUY':
                return abs(num)
            elif self.side == 'SELL':
                return - abs(num)
        else:
            return abs(num)

    def get_value(self, rounding: int = 4, signed=True) -> float:
        """Returns total value of the order.
        
        Parameters
        ----------
        rounding : int
            Default value is 4.
            Determines the amount of rounding of the total value of the
            order.

        signed : bool
            Default value is True.
            Determine wheter the returned value is signed or not.

        Returns
        -------
            : float
            Returns total value of the order.
        """
        return round(
            self.get_numeric_amount(signed = signed) *\
                self.get_price(numeric=True)
                ,
                rounding
                )

    def to_dict(self, numeric=False) -> dict:
        """Returns a dictionary representation of order.
        
        The method returns the dictionary representation of the order.
        """
        d = {}
        d['symbol'] = self.symbol.symbol
        d['side'] = self.side
        d['price'] = self.get_price(numeric=numeric)
        d['amount'] = self.get_amount(numeric=numeric)
        d['type_'] = self.type_
        return d

    def serialize(
        self,
        keys: list = None
        ) -> dict:
        """Returns the serialized version of Order object.
        
        The returned dictionary is used to consume in API request.

        Parameters
        ----------
        keys : list
            Default value is None.
            The `keys` parameter is a list of attributes that is needed to
            be serialized.

        Returns
        -------
            : dict
            Returns the serialized data of Order

        """
        if keys is None:
            keys = ['symbol', 'side', 'amount', 'price']
        if self.type_ == 'MARKET':
            raise NotImplementedError(
                "for Order of type_ = 'MARKET' the serialize"
                " method is not implemented"
                )
        d = self.to_dict(numeric=False)
        return dict((k, d[k]) for k in keys if k in d)

    def serialize_full_depth(self) -> dict:
        """Returns the full depth serialized Order data.

        It serialize the Order attributes and it also serialized the `symbol`
        property of the Order by its own serialize_full_depth method.

        Returns
        -------
            : dict
            Fully serialized in depth Order object and its attributes

        """
        d = {}
        d['symbol'] = self.symbol.serialize_full_depth()
        d['side'] = self.side
        d['price'] = self.get_price(numeric=True)
        d['amount'] = self.get_amount(numeric=True)
        d['type_'] = self.type_
        return d

    def deserialize(self, serialized_data: dict):
        """Deserilize serialized_data to Order object.

        The method deserializes data and sets the Order object attributes 
        based on the data.

        Parameters
        ----------
        serialized_data : dict
            The serialized data which is probably produced by the
            `serialize_full_depth` method of Order object.

        Returns
        -------
        self : Order
            Returns this object (self) after setting its attributes using
            serialized data.
        """
        self.symbol = self.symbol.deserialize(serialized_data['symbol'])
        self.side = serialized_data['side']
        self.type_ = serialized_data['type_']
        self.price = Price(
            serialized_data['price'],
            self.symbol.digits,
            self.symbol.precision
            )
        self.amount = Amount(
            serialized_data['amount'],
            self.symbol.amount_digits,
            self.symbol.amount_precision
            )
        return self

    def __eq__(self, other) -> bool:
        """Overloads == operator for Order

        Two Order objects are equal if and only if all of their attributes
        are equal.

        Returns
            : bool
        """
        if (
            self.symbol == other.symbol and
            self.side == other.side and
            self.amount == other.amount and 
            self.price == other.price and 
            self.type_ == other.type_
            ):
            return True
        else:
            return False

    def __str__(self) -> str:
        s = '| '
        s += self.side.ljust(4) + '| '
        s += str(self.get_numeric_amount()).\
            rjust(self.symbol.digits + 2) + '|'
        s += self.get_price(numeric=False).\
            rjust(self.symbol.amount_digits + 2) + '|'
        s += str(self.get_value()).rjust(8) + '|'
        return s

    def to_text(self) -> str:
        """Returns an string representation of Order.

        Returns
        -------
            : str
        """
        return str(self)

    def __repr__(self) -> str: # TODO: write a test and update Price and Amount by defining __repr__ method
        return f"Order({repr(self.symbol)}, '{self.side}', {repr(self.price)}, {repr(self.amount)}, '{self.type_}')"


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)