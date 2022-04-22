"""A module to manipulate Amount.
"""

from .number_string import NumberString

class Amount(NumberString):
    """ """
    
    def __init__(self, number, digits=9, precision=8):
        super().__init__(
            number=number,
            digits=digits,
            precision=precision
        )

 
    def increase(self, percentage: float = 0.01):
        """Return a new Amount objects with increased percentage.

        The method returns a new Amount object such that the `precision` and
        `digits` attributes are same as this Amount object. The `number`
        attribute of the new amount object is calculated as follows:
        new object number = this object number * (1 + percentage + fee).

        Parameters
        ----------
        percentage : float
             (Default value = 0.01)
             The ratio amount to increase the Amount number by mulitiplication.


        Returns
        -------
         : Amount
            Reutrns a Amount objects with incremented number

        """
        return Amount(
            number=self.number * (1 + percentage),
            digits=self.digits,
            precision=self.precision,
        )


    def decrease(self, percentage: float = 0.01):
        """Return a new Amount objects with decreased percentage.

        The method returns a new Amount object such that the `precision` and
        `digits` attributes are same as this Amount object. The `number`
        attribute of the new Amount object is calculated as follows:
        new object number = this object number / (1 + percentage + fee).

        The new object is a Amount which is when incremented by the
        `percentage` with the give `fee` will result in this Amount object
        number.

        Parameters
        ----------
        percentage : float
             (Default value = 0.01)
             The ratio amount to decrease the Amount number by division.
        fee : flaot
             (Default value = 0.004)
             The ratio amount of fee. This is useful in cases where there is a
             fee for tradings and you want to find the effective Amount to sell
             or buy considering fees by exchanges.

        Returns
        -------
         : Amount
            Reutrns a Amount objects with decreased number

        """
        return Amount(
            number=self.number / (1 + percentage),
            digits=self.digits,
            precision=self.precision,
        )

    def get_amount(self) -> str:
        """Returns the Amount as string"""
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
        return self.get_Amount()

    def __repr__(self):
        return f"Amount({self.number}, {self.digits}, {self.precision})"
    

