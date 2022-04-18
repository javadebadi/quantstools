"""A module for order history
"""
from datetime import datetime
from pytz import timezone
from pytz import utc
from .price import Price
from .order import Order
from .exception import OrderCancelError

class OrderHistory(Order):

    def __init__(
        self,
        id_,
        symbol: str,
        side: str,
        price: Price,
        amount: str,
        mili_unixtime: int,
        is_active: bool = True,
        is_cancelled: bool = False,
        type_: str = 'LIMIT',
        ):
        self.id_ = id_
        self.is_active = is_active
        self.is_cancelled = is_cancelled
        self.mili_unixtime = mili_unixtime
        super().__init__(
            symbol=symbol,
            side=side,
            price=price,
            amount=amount,
            type_=type_    
        )

    @classmethod
    def from_order(
        cls,
        id_: str,
        order: Order,
        mili_unixtime: int,
        is_active: bool = True,
        is_cancelled: bool = False,
        ):
        return OrderHistory(
            id_=id_,
            symbol=order.symbol,
            amount=order.amount,
            price=order.price,
            side=order.side,
            type_=order.type_,
            mili_unixtime=mili_unixtime,
            is_active=is_active,
            is_cancelled=is_cancelled,
            )

    @property
    def id_(self) -> str:
        return self._id_

    @id_.setter
    def id_(self, id_) -> None:
        assert type(id_) == str
        self._id_ = id_

    @property
    def mili_unixtime(self) -> int:
        return self._mili_unixtime

    @mili_unixtime.setter
    def mili_unixtime(self, mili_unixtime) -> None:
        assert type(mili_unixtime) == int
        self._mili_unixtime = mili_unixtime

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, is_active: bool) -> None:
        assert type(is_active) == bool
        self._is_active = is_active

    @property
    def is_cancelled(self) -> bool:
        return self._is_cancelled

    @is_cancelled.setter
    def is_cancelled(self, is_cancelled: bool) -> None:
        assert type(is_cancelled) == bool
        self._is_cancelled = is_cancelled

    def cancel(self):
        if self.is_active:
            self.is_cancelled = True
            self.deactivate()
        else:
            raise OrderCancelError(
                f"Non-active order with id = '{self.id_}' could not be cancelled"
                )

    def deactivate(self):
        self.is_active = False

    def get_value(self, rounding: int = None) -> float:
        if rounding is None:
            rounding = self.price.precision
        else:
            assert rounding >= 0 and type(rounding) == int
        return round(float(self.price.get_price()) * float(self.amount), rounding)

    def get_mili_unixtime(self) -> int:
        return self.mili_unixtime

    def get_unixtime(self, how='int') -> int:
        assert how in ['int', 'round']
        if how == 'int':
            return int(self.mili_unixtime / 1000)
        elif how == 'round':
            return int(round(self.mili_unixtime / 1000, 0))

    def get_utcdatetime(self):
            return datetime.utcfromtimestamp(self.get_unixtime())

    def get_date_in_timezone(self, tz='America/Montreal'):
        utc_dt = self.get_utcdatetime()
        aware_utc_dt = utc_dt.replace(tzinfo=utc)
        tz = timezone(tz)
        dt = aware_utc_dt.astimezone(tz)
        return dt

    def to_dict(self, numeric=False) -> dict:
        d = super().to_dict(numeric=numeric)
        d['id'] = self.id_
        return d