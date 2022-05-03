"""A module for Stock Symbols or Tickers
"""

class Symbol:

    """Class to define a Symbol or Ticker
    
    Example
    -------
    >>> symbol = Symbol('VRA-USDT', 9, 8, 12, 6)
    >>> print(symbol)
    VRA-USDT
    >>> symbol.digits
    9
    >>> symbol.precision
    8
    >>> symbol.amount_digits
    12
    >>> symbol.amount_precision
    6
    """

    def __init__(
        self,
        symbol: str,
        digits: int,
        precision: int,
        amount_digits: int,
        amount_precision: int,
        ):
        self.symbol = symbol
        self.digits = digits
        self.precision = precision
        self.amount_digits = amount_digits
        self.amount_precision = amount_precision

    @property
    def symbol(self) -> str:
        """Returns the `symbol` property attribute
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str) -> None:
        """Property setter for `symbol`

        The `symbol` attribute of a Symbol object must be string.
        The property setter checks the value before setting the `symbol`
        attribute. Currently it is required the type of `symbol` attribute
        to be sting.

        Parameters
        ----------
        symbol : str

        Returns
        -------
        None

        Raises
        ------
        TypeError
            Raises `TypeError` when the type of symbol argument is not
            correct.
        """
        if type(symbol) != str:
            raise TypeError(
                "Expected symbol of type 'str'"
                f" but got type '{symbol.__class__.__name__}'"
            )
        self._symbol = symbol

    @property
    def digits(self) -> int:
        """Returns the `digits` property attribute"""
        return self._digits

    @digits.setter
    def digits(self, digits: int):
        """Property setter for `digits`

        Parameters
        ----------
        digits : int
            Maximum number of digits in price of a symbol
            
        Returns
        -------
        None

        Raises
        ------
        TypeError
            Raises TypeError when type of digits parameter is not integer.
        
        """
        if type(digits) == int:
            self._digits = digits
        else:
            raise TypeError(
                f"Expected digits of type 'int'"
                f" but got type '{digits.__class__.__name__}'"
                )

    @property
    def amount_digits(self) -> int:
        """Returns the `amount_digits` property attribute"""
        return self._amount_digits

    @amount_digits.setter
    def amount_digits(self, amount_digits: int):
        """Property setter for `amount_digits` attribute

        Parameters
        ----------
        amount_digits : int
            Maximum number of digits for amount of symbol.
            
        Returns
        -------
        None

        Raises
        ------
        TypeError
            Raises type error when type of `amount_digits` parameter is
            not integer.
        
        """
        if type(amount_digits) == int:
            self._amount_digits = amount_digits
        else:
            raise TypeError(
                f"Expected amount_digits of type 'int'"
                f" but got type '{amount_digits.__class__.__name__}'"
                )

    @property
    def precision(self) -> int:
        """Returns the precision attribute"""
        return self._precision

    @precision.setter
    def precision(self, precision: int):
        """

        Parameters
        ----------
        precision : int

        Returns
        -------
        None

        Raises
        ------
        TypeError

        
        """
        if type(precision) == int:
            self._precision = precision
        else:
            raise TypeError(
                f"Expected precision of type int"
                f" but got type '{precision.__class__.__name__}'"
                )

    @property
    def amount_precision(self) -> int:
        """Returns the amount_precision attribute"""
        return self._amount_precision

    @amount_precision.setter
    def amount_precision(self, amount_precision: int):
        """

        Parameters
        ----------
        precision : int

        Returns
        -------
        None

        Raises
        ------
        TypeError

        
        """
        if type(amount_precision) == int:
            self._amount_precision = amount_precision
        else:
            raise TypeError(
                f"Expected amount_precision of type int"
                f" but got type '{amount_precision.__class__.__name__}'"
                )

    def to_dict(self) -> dict:
        d = {}
        d['symbol'] = self.symbol
        d['digits'] = self.digits
        d['precision'] = self.precision
        d['amount_digits'] = self.amount_digits
        d['amount_precision'] = self.amount_precision
        return d

    def __eq__(self, other) -> bool:
        if not isinstance(other, Symbol):
            return False
        if (
            self.symbol == other.symbol &
            self.digits == other.digits &
            self.precision == other.precision &
            self.amount_digits == other.amount_digits &
            self.amount_precision == other.amount_precision
        ):
            return True
        else:
            return False

    def __str__(self) -> str:
        return f'{self.symbol}'

    def __repr__(self) -> str:
        return f"Symbol('{self.symbol}', {self.digits}, {self.precision}, {self.amount_digits}, {self.amount_precision})"


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)