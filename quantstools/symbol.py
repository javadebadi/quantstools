"""A module for Symbols
"""

class Symbol:

    def __init__(
        self,
        symbol: str,
        ):
        self.symbol = symbol

    @property
    def symbol(self) -> str:
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str) -> None:
        assert type(symbol) == str
        self._symbol = symbol

    def to_dict(self) -> dict:
        d = {}
        d['symbol'] = self.symbol
        return d

    def __eq__(self, other) -> bool:
        if self.symbol == other.symbol:
            return True
        else:
            return False

    def __str__(self) -> str:
        return f'{self.symbol}'
