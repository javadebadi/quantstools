"""A module to manage orders
"""

from .price import Price

class Order:

    def __init__(
        self,
        symbol: str,
        side: str,
        price: Price,
        amount: str,
        type_: str = 'LIMIT',
        ):
        self.symbol = symbol
        self.side = side
        self.price = price
        self.amount = amount
        self.type_ = type_


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
    def price(self) -> Price:
        return self._price

    @price.setter
    def price(self, price) -> None:
        assert isinstance(price, Price)
        self._price = price

    @property
    def amount(self) -> str:
        return self._amount

    @amount.setter
    def amount(self, amount) -> None:
        assert type(amount) == str
        self._amount = amount

    @property
    def type_(self) -> str:
        return self._type_

    @type_.setter
    def type_(self, type_) -> None:
        assert type_ in ['LIMIT', 'MARKET']
        self._type_ = type_

    def get_price(self) -> Price:
        return self.price.get_price()

    def get_numeric_amount(self) -> float:
        if self.side == 'BUY':
            return abs(float(self.amount))
        elif self.side == 'SELL':
            return - abs(float(self.amount))

    def get_value(self) -> float:
        return self.get_numeric_amount() * float(self.get_price())

    def to_dict(self, numeric=False) -> dict:
        d = {}
        d['symbol'] = self.symbol
        d['side'] = self.side
        d['price'] = self.get_price()
        d['amount'] = self.amount
        if numeric is True:
            d['price'] = float(d['price'])
            d['amount'] = float(d['amount'])
        d['type_'] = self.type_
        return d