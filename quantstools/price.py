"""A module to manipulate Price.
"""

from unicodedata import decimal


class Price:
    """ """
    
    def __init__(self, number, digits=9, precision=8):
        self.digits = digits
        self.precision = precision
        self.number = number

    @property
    def number(self) -> float:
        """Returns the number attribute"""
        return self._number

    @number.setter
    def number(self, number: float):
        """

        Parameters
        ----------
        number : float

        Returns
        -------

        Raises
        ------
        TypeError

        
        """
        if type(number) == float or type(number) == int:
            self._number = round(float(number), self.precision)
        else:
            raise TypeError(
                f"Expected number of type int or float"
                f" but got type '{number.__class__.__name__}'"
                )
                
        if len(str(self._number).split('.')[0]) > self.integer_digits:
            raise AssertionError(
                f"The number of integer part "
                f"'{str(self._number).split('.')[0]}' "
                f"could not be bigger than {self.integer_digits}"
                )

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

    @property
    def integer_digits(self) -> int:
        """Returns the number of integer digits of the `self.number`"""
        return self.digits - self.precision
        
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
        if self.number > 1:
            int_part = str(self.number).split('.')[0]
        else:
            int_part = '0'

        decimal_part = str(self.number).split('.')[1][:self.precision].ljust(self.precision, '0')

        return (int_part + '.' + decimal_part)
        
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
    

