"""A module to manipulate Numbers such as they are strings.
"""


class NumberString:
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
        """Return a new NumberString objects with increased percentage.

        The method returns a new NumberString object such that the `precision` and
        `digits` attributes are same as this NumberString object. The `number`
        attribute of the new NumberString object is calculated as follows:
        new object number = this object number * (1 + percentage + fee).

        Parameters
        ----------
        percentage : float
             (Default value = 0.01)
             The ratio amount to increase the NumberString number by mulitiplication.
        fee : flaot
             (Default value = 0.004)
             The ratio amount of fee. This is useful in cases where there is a
             fee for tradings and you want to find the effective NumberString to sell
             or buy considering fees by exchanges.

        Returns
        -------
         : NumberString
            Reutrns a NumberString objects with incremented number

        """
        return NumberString(
            number=self.number * (1 + percentage + fee),
            digits=self.digits,
            precision=self.precision,
        )


    def decrease(self, percentage: float = 0.01, fee: float = 0.004):
        """Return a new NumberString objects with decreased percentage.

        The method returns a new NumberString object such that the `precision` and
        `digits` attributes are same as this NumberString object. The `number`
        attribute of the new NumberString object is calculated as follows:
        new object number = this object number / (1 + percentage + fee).

        The new object is a NumberString which is when incremented by the
        `percentage` with the give `fee` will result in this NumberString object
        number.

        Parameters
        ----------
        percentage : float
             (Default value = 0.01)
             The ratio amount to decrease the NumberString number by division.
        fee : flaot
             (Default value = 0.004)
             The ratio amount of fee. This is useful in cases where there is a
             fee for tradings and you want to find the effective NumberString to sell
             or buy considering fees by exchanges.

        Returns
        -------
         : NumberString
            Reutrns a NumberString objects with decreased number

        """
        return NumberString(
            number=self.number / (1 + percentage + fee),
            digits=self.digits,
            precision=self.precision,
        )

    def get_number(self) -> str:
        """Returns the numbers as string"""
        if self.number >= 1.00000000000000:
            int_part = str(self.number).split('.')[0]
        else:
            int_part = '0'

        decimal_part = str(self.number).split('.')[1][:self.precision].ljust(self.precision, '0')

        return (int_part + '.' + decimal_part)

    def get_numeric_number(self) -> float:
        """Returns the numeric value of number property
        """
        return self.number
        
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
        return self.get_number()

    def __repr__(self):
        return f"NumberString({self.number}, {self.digits}, {self.precision})"
    

