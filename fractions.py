from decimal import Decimal


class fraction:
    def __init__(self, n, d):
        """the fractions will be simplified after creating"""

        negative = 1
        if (n < 0) ^ (d < 0):
            negative = -1
        n, d = abs(n), abs(d)

        hcf = fraction.__hcf(n, d)
        self.n = n // hcf * negative
        self.d = d // hcf

    def __str__(self):
        n = self.numerator()
        d = self.denominator()

        return f"{n}/{d}"

    def __add__(self, other):
        """adding two fractions together"""
        other = fraction.__clarify_fraction(other)
        n = self.n
        d = self.d
        n_ = other.n
        d_ = other.d

        result = fraction(n*d_ + n_*d, d*d_)
        return result

    def __sub__(self, other):
        """subtracting two fractions from each other"""
        return self + (other*-1)

    def __mul__(self, other):
        """multiplying fraction by fraction, int or float"""
        other = fraction.__clarify_fraction(other)
        n = self.n
        d = self.d
        n_ = other.n
        d_ = other.d
        return fraction(n*n_, d*d_)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        """divides self by other"""
        other = fraction.__clarify_fraction(other)
        return self * ~other

    def __rtruediv__(self, other):
        """divids other by self"""
        other = fraction.__clarify_fraction(other)
        return other * ~self

    def __pow__(self, power):
        if isinstance(power, int):
            def exp_by_sqr(x, p):
                if p == -1:
                    return ~x
                elif p == 0:
                    return fraction(1, 1)
                elif p == 1:
                    return x
                elif p % 2 == 0:
                    return exp_by_sqr(x * x, p // 2)
                elif p % 2 != 0:
                    return x * exp_by_sqr(x * x, (p - 1) // 2)
            return exp_by_sqr(self, power)

    def __and__(self, other):
        """naive addition of fractions"""
        n = self.n
        d = self.d
        n_ = other.n
        d_ = other.d
        return fraction(n+n_, d+d_)

    def __abs__(self):
        """returns Decimal value of fraction"""
        return self.get_true_value()

    def __invert__(self):
        """equivalent to 1/'self'"""
        n = self.n
        d = self.d

        return fraction(d, n)

    def numerator(self):
        """returns the numerator of a fraction"""
        return self.n

    def denominator(self):
        """returns the denominator of a fraction"""
        return self.d

    def get_true_value(self):
        """return true value in Decimal"""
        n = self.n
        d = self.d
        return Decimal(n) / Decimal(d)

    @staticmethod
    def estimate_fraction(num):
        """returns a fraction estimation of num"""
        num = Decimal(repr(num))  # set num to 'Decimal' type
        integer = num // 1  # integer is the whole number part of num
        dec = num % 1  # num is the decimal part of num
        bot = fraction(0, 1)  # the lowest number dec could be
        top = fraction(1, 1)  # the highest number dec could be
        mid = bot & top  # mid is the naive addition of bot and top
        while mid.get_true_value() != dec:  # while mid is not a good estimation of dec
            if mid.get_true_value() < dec:  # if mid is smaller than dec, increase size
                bot = mid
                mid = mid & top
            elif mid.get_true_value() > dec:  # if mid is larger than dec, decrease size
                top = mid
                mid = bot & mid
        mid.n = mid.n + integer*mid.d  # multiplies integer back into the estimation
        return mid

    @staticmethod
    def __hcf(a, b):
        """returns highest common factor, private method"""
        rt = 1
        i = 1
        c = a if a < b else b
        jump = 2
        while i < c:
            # i only has to be prime number
            # finding prime numbers is very inefficient so we check numbers either side of multiples of 6
            # as that is the only place a prime number occurs
            if i < 5:
                i += 1
            elif jump == 2:
                i += jump
                jump = 4
            elif jump == 4:
                i += jump
                jump = 2

            if a % i == 0 and b % i == 0:
                a = a // i
                b = b // i
                rt *= i
                i = 1
        return rt

    @staticmethod
    def __clarify_fraction(value):
        """returns a fractional value of an int of a float, private method"""
        if isinstance(value, int):
            return fraction(value, 1)
        if isinstance(value, float):
            return fraction.estimate_fraction(value)
        if isinstance(value, fraction):
            return value
