import pytest
import unittest
from quantstools.order import Symbol


class TestSymbol:

    def test_symbol_init(self):
        s = Symbol('BTC-USDT', 12, 4, 12, 6)
        assert s.symbol == 'BTC-USDT'
        assert s.precision == 4
        assert s.digits == 12
        assert s.amount_digits == 12
        assert s.amount_precision == 6

    def test_symbol_property_raises_error(self):
        with pytest.raises(AssertionError) as exc_info:
            s = Symbol(6594, 12, 4, 12, 6)

    def test_symbol_eq(self):
        s0 = Symbol('BTC-USDT', 12, 4, 12, 6)
        s1 = Symbol('BTC-USDT', 12, 4, 12, 6)
        s2 = Symbol('ETH-USDT', 12, 4, 12, 6)
        assert s1 == s0
        assert s2 != s0

    def test_to_dict(self):
        s = Symbol('BTC-USDT', 12, 4, 12, 6)
        assert s.to_dict() ==  {'symbol': 'BTC-USDT', 'digits': 12, 'precision': 4, 'amount_digits': 12, 'amount_precision': 6}