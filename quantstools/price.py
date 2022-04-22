"""A module to manipulate Price.
"""

from .number_string import NumberString

class Price(NumberString):
    """ """
    
    def __init__(self, number, digits=9, precision=8):
        super().__init__(
            number=number,
            digits=digits,
            precision=precision
        )

 
    def increase(self, percentage: float = 0.01, fee: float = 0.004):
        """Return a new Price objects with increased percentage.

        The method returns a new Price object such that the `precision` and
        `digits` attributes are same as this Price object. The `number`
        attribute of the new price object is calculated as follows:
        new object number = this object number * (1 + percentage + fee).

        Parameters
        ----------
        percentage : float
             (Default value = 0.01)
             The ratio amount to increase the price number by mulitiplication.
        fee : flaot
             (Default value = 0.004)
             The ratio amount of fee. This is useful in cases where there is a
             fee for tradings and you want to find the effective price to sell
             or buy considering fees by exchanges.

        Returns
        -------
         : Price
            Reutrns a Price objects with incremented number

        """
        return Price(
            number=self.number * (1 + percentage + fee),
            digits=self.digits,
            precision=self.precision,
        )


    def decrease(self, percentage: float = 0.01, fee: float = 0.004):
        """Return a new Price objects with decreased percentage.

        The method returns a new Price object such that the `precision` and
        `digits` attributes are same as this Price object. The `number`
        attribute of the new price object is calculated as follows:
        new object number = this object number / (1 + percentage + fee).

        The new object is a price which is when incremented by the
        `percentage` with the give `fee` will result in this Price object
        number.

        Parameters
        ----------
        percentage : float
             (Default value = 0.01)
             The ratio amount to decrease the price number by division.
        fee : flaot
             (Default value = 0.004)
             The ratio amount of fee. This is useful in cases where there is a
             fee for tradings and you want to find the effective price to sell
             or buy considering fees by exchanges.

        Returns
        -------
         : Price
            Reutrns a Price objects with decreased number

        """
        return Price(
            number=self.number / (1 + percentage + fee),
            digits=self.digits,
            precision=self.precision,
        )

    def get_price(self) -> str:
        """Returns the price as string"""
        return super().get_number()
        
    def __lt__(self, other):
        return self.number < other.number
    
    def __gt__(self, other):
        return self.number > other.number
    
    def __le__(self, other):
        return self.number <= other.number

    def __ge__(self, other):
        return self.number >= other.number
    
    def __eq__(self, other):
        return self.number == other.number
        
    def __str__(self):
        return self.get_price()

    def __repr__(self):
        return f"Price({self.number}, {self.digits}, {self.precision})"
    

