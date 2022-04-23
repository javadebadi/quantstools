"""A module to manage orders
"""

from email.mime import base
from .order_history_collection import OrderHistoryCollection
from .order_collection import OrderCollection
from .order import Order
from .order_history import OrderHistory
from .price import Price
from .amount import Amount
from .symbol import Symbol

class OrderManager:

    def __init__(
        self,
        symbol: Symbol,
        amount_digits: int,
        amount_precision: int,
        ):
        self._symbol = symbol
        self._digits = symbol.digits
        self._precision = symbol.precision
        self._amount_digits = amount_digits
        self._amount_precision = amount_precision
        self._ohc = OrderHistoryCollection(self.symbol)
        self._oc = OrderCollection(self.symbol)

    @property
    def symbol(self) -> Symbol:
        return self._symbol

    @property
    def digits(self) -> int:
        return self._digits

    @property
    def precision(self) -> int:
        return self._precision

    @property
    def ohc(self) -> OrderHistoryCollection:
        return self._ohc

    @property
    def amount_digits(self) -> int:
        return self._amount_digits

    @property
    def amount_precision(self) -> int:
        return self._amount_precision

    def generate_buy_limit_order(
        self,
        price: float,
        amount: float,
        ) -> Order:
        return Order(
            symbol=self.symbol,
            side='BUY',
            price=Price(price, self.digits, self.precision),
            amount=Amount(amount, self.amount_digits, self.amount_precision),
            type_='LIMIT',
        )

    def generate_buy_limit_orders_triangle(
        self,
        max_price: float,
        min_amount: float,
        n_orders: int = 10,
        price_decrement_rate: float = 0.01,
        amount_increment_rate: float = 0.04,
        ):
        base_price = Price(max_price, self.digits, self.precision)
        base_amount = Amount(min_amount, self.amount_digits, self.amount_precision)
        oc = OrderCollection(self.symbol)
        price = base_price
        amount = base_amount
        for _ in range(n_orders):
            oc.add_order(
                self.generate_buy_limit_order(
                    float(price.get_price()),
                    float(amount.get_amount()),
                    )
            )
            price = price.decrease(price_decrement_rate)
            amount = amount.increase(amount_increment_rate)
        return oc

    def get_orders_history(
        self,
        list_of_dicts,
        params_mapping: dict = None,
        ) -> None:
        """Gets orders history"""
        if params_mapping is None:        
            params_mapping = {
                'id_': 'id_',
                'symbol': 'symbol',
                'price': 'price',
                'side': 'side',
                'amount': 'amount',
                'mili_unixtime': 'mili_unixtime',
                'is_cancelled': 'is_cancelled',
                'is_active': 'is_active',
                }
        for order_data in list_of_dicts:
            d = {}
            for key, value in params_mapping.items():
                d[key] = order_data.get(value)
            if d['symbol'] != self.symbol.symbol:
                raise ValueError("Wrong Symbol!")
            d['symbol'] = self.symbol
            d['price'] = Price(float(d['price']), self.symbol.digits, self.symbol.precision)
            d['amount'] = Amount(float(d['amount']), self.amount_digits, self.amount_precision)
            o = OrderHistory(**d)
            self._ohc.add_order_history(o)


