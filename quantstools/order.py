"""A module to manage orders
"""

from .price import Price
from .amount import Amount
from .symbol import Symbol

class Order:

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
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str) -> None:
        assert isinstance(symbol, Symbol)
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
    def amount(self) -> Amount:
        return self._amount

    @amount.setter
    def amount(self, amount) -> None:
        assert isinstance(amount, Amount)
        self._amount = amount

    @property
    def type_(self) -> str:
        return self._type_

    @type_.setter
    def type_(self, type_) -> None:
        assert type_ in ['LIMIT', 'MARKET']
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

    def __eq__(self, other) -> bool:
        if self.to_dict() == other.to_dict():
            return True
        else:
            return False

    def __str__(self) -> str:
        return f'{self.amount.get_amount()} | {self.get_price()} | {self.get_value()}'
