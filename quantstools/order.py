"""A module to manage orders
"""

from .price import Price

class Order:

    def __init__(
        self,
        symbol,
        side,
        price,
        ):
        self.symbol = symbol
        self.side = side
        self.price = price

    @property
    def symbol(self) -> str:
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str) -> None:
        assert type(symbol) == str
        self._symbol = symbol

    @property
    def side(self) -> str:
        return self._side

    @side.setter
    def side(self, side: str) -> None:
        assert side in ['BUY', 'SELL']
        self._side = side

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        assert isinstance(price, Price)
        self._price = price

    def get_price(self):
        return self.price.get_price()

    def to_dict(self) -> dict:
        d = {}
        d['symbol'] = self.symbol
        d['side'] = self.side
        d['price'] = self.get_price()
        return d