"""A module for Symbols
"""

class Symbol:

    def __init__(
        self,
        symbol: str,
        digits: int,
        precision: int,
        ):
        self.symbol = symbol
        self.digits = digits
        self.precision = precision

    @property
    def symbol(self) -> str:
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str) -> None:
        assert type(symbol) == str
        self._symbol = symbol

    @property
    def digits(self) -> int:
        """Returns the digits attribute"""
        return self._digits

    @digits.setter
    def digits(self, digits: int):
        """

        Parameters
        ----------
        digits : int
            
        Returns
        -------
        None

        Raises
        ------
        TypeError
        
        """
        if type(digits) == int:
            self._digits = digits
        else:
            raise TypeError(
                f"Expected digits of type int"
                f" but got type '{digits.__class__.__name__}'"
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

    def to_dict(self) -> dict:
        d = {}
        d['symbol'] = self.symbol
        d['digits'] = self.digits
        d['precision'] = self.precision
        return d

    def __eq__(self, other) -> bool:
        if self.symbol == other.symbol:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f'{self.symbol}'
