from decimal import Decimal
from math import gcd
import inspect


class fraction:
    class PrivateAttribute(Exception):
        pass

    def __init__(self, n, d=1):
        """the fractions will be simplified after initialisation"""

        # if any of the terms are fractions or floats the code will simplify
        if isinstance(n, fraction) or isinstance(d, fraction) or isinstance(n, float) or isinstance(d, float):
            n = fraction.__clarify_fraction(n)
            d = fraction.__clarify_fraction(d)
            new_fraction = n / d
            n, d = new_fraction.numerator, new_fraction.denominator

        # if the denominator is zero the raise error
        if d == 0:
            text = "cannot create fraction with a denominator of zero (cannot divide by zero)"
            raise ZeroDivisionError(text)

        if n == 0:  # is the numerator is zero, simplify to 0/1
            self.numerator = 0
            self.denominator = 1
        else:
            negative = 1
            if (n < 0) ^ (d < 0):  # if there is one negative across the attributes
                negative = -1  # saves if the result needs to be negative
            n, d = abs(n), abs(d)
            hcf = gcd(n, d)  # highest common factor = greatest common denominator
            self.numerator = n // hcf * negative  # divides both attributes by hcf and adds the negative if needed
            self.denominator = d // hcf

    def __setattr__(self, key, value):
        """checks if call is coming from outer scope and returns an error if it is"""
        x = inspect.currentframe()
        x = inspect.getouterframes(x, 2)
        if x[1][3] not in self.__dir__():  # if the call is not coming from a defined method, then raise error
            text = "don't change attributes from outer scope"
            raise self.PrivateAttribute(text)
        self.__dict__[key] = value

    def __str__(self):
        """casting to string"""
        n = self.numerator
        d = self.denominator

        return f"{n}/{d}"

    def __int__(self):
        """casting to int (rounding down)"""
        return int(self.get_decimal_value())

    def __float__(self):
        """casting to float"""
        return float(self.get_decimal_value())

    def __bool__(self):
        """only returns false if value is zero"""
        return False if self == 0 else True

    def __add__(self, other):
        """adding two fractions together"""
        other = fraction.__clarify_fraction(other)
        n = self.numerator
        d = self.denominator
        n_ = other.numerator
        d_ = other.denominator

        result = fraction(n*d_ + n_*d, d*d_)
        return result

    def __radd__(self, other):
        """refer to __add__"""
        return fraction.__add__(self, other)

    def __sub__(self, other):
        """subtracting two fractions from each other"""
        return self + (other*-1)

    def __rsub__(self, other):
        """refer to __sub__"""
        return other + (self*-1)

    def __mul__(self, other):
        """multiplying fraction by fraction, int or float"""
        other = fraction.__clarify_fraction(other)
        n = self.numerator
        d = self.denominator
        n_ = other.numerator
        d_ = other.denominator
        return fraction(n*n_, d*d_)

    def __rmul__(self, other):
        """refer to __mul__"""
        return self.__mul__(other)

    def __truediv__(self, other):
        """divides self by other"""
        other = fraction.__clarify_fraction(other)
        return self * ~other

    def __rtruediv__(self, other):
        """divides other by self"""
        other = fraction.__clarify_fraction(other)
        return other * ~self

    def __floordiv__(self, other):
        """returns a rounded down version of self / other"""
        return int(self / other)

    def __rfloordiv__(self, other):
        return int(other / self)

    def __mod__(self, other):
        """returns the remainder of self // other"""
        return self - (other * (self // other))

    def __rmod__(self, other):
        return other - (self * (other // self))

    def __pow__(self, power):
        """a fraction to the power of an int"""
        if isinstance(power, int):  # exponential by squaring
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
        n = self.numerator
        d = self.denominator
        n_ = other.numerator
        d_ = other.denominator
        return fraction(n+n_, d+d_)

    def __abs__(self):
        """returns Decimal value of fraction"""
        return self.get_decimal_value()

    def __round__(self, n=None):
        """rounds the decimal value"""
        return round(self.get_decimal_value(), n)

    def __pos__(self):
        """does nothing"""
        return self

    def __neg__(self):
        """returns fraction times minus one"""
        return self * -1

    def __invert__(self):
        """equivalent to 1/self"""
        n = self.numerator
        d = self.denominator

        return fraction(d, n)  # flips numerator and denominator

    def __eq__(self, other):
        """returns true is fractions are equal"""
        other = fraction.__clarify_fraction(other)
        if self.numerator == other.numerator and self.denominator == other.denominator:
            return True
        return False

    def __gt__(self, other):
        """returns true if first fraction is greater than the second value"""
        self_ = fraction.__clarify_fraction(self)
        other = fraction.__clarify_fraction(other)
        if self_.numerator * other.denominator > self_.denominator * other.numerator:
            return True
        return False

    def __lt__(self, other):
        """returns true if first fraction is less than the second value"""
        return fraction.__gt__(other, self)  # calls greater than and passes vars in reverse order

    def __ge__(self, other):
        """returns true if first fraction is greater than or equal to the second value"""
        self_ = fraction.__clarify_fraction(self)
        other = fraction.__clarify_fraction(other)
        if (self_.numerator == other.numerator and self_.denominator == other.denominator) or (self_.numerator * other.denominator > self_.denominator * other.numerator):
            return True
        return False

    def __le__(self, other):
        """returns true if first fraction is less than or equal to the second value"""
        return fraction.__ge__(other, self)  # calls greater than and passes vars in reverse order

    def get_continued_fraction(self):
        """returns the integers of a continued fraction"""
        n = self.numerator
        d = self.denominator

        if d == 1:
            return tuple([n])
        else:
            return (n // d, *(fraction(d, n % d).get_continued_fraction()))

    def get_decimal_value(self):
        """return value in Decimal"""
        n = self.numerator
        d = self.denominator
        return Decimal(n) / Decimal(d)

    def is_int(self):
        """returns true if the fraction could be writen as a int"""
        if self.denominator == 1:
            return True
        return False

    def does_terminate(self):
        """returns true if the decimal expansion terminates"""
        flag = True
        for i in fraction.__get_prime_factors(self.denominator):
            if i != 2 and i != 5:
                flag = False

        return flag

    @staticmethod
    def estimate_fraction(num):
        """returns a fraction estimation of num"""
        num = Decimal(repr(num))  # set num to 'Decimal' type
        integer = int(num // 1)  # integer is the whole number part of num
        dec = num % 1  # num is the decimal part of num
        if dec == 0:  # if dec is zero then fraction has a denominator of 1
            return fraction(integer, 1)
        bot = fraction(0, 1)  # the lowest number dec could be
        top = fraction(1, 1)  # the highest number dec could be
        mid = bot & top  # mid is the naive addition of bot and top
        while round(mid.get_decimal_value(), 11) != round(dec, 11):  # while mid is not a good estimation of dec
            if mid.get_decimal_value() < dec:  # if mid is smaller than dec, increase size
                bot = mid
                mid = mid & top
            elif mid.get_decimal_value() > dec:  # if mid is larger than dec, decrease size
                top = mid
                mid = bot & mid
        mid.numerator = mid.numerator + integer * mid.denominator  # multiplies integer back into the estimation
        return mid

    @staticmethod
    def __get_prime_factors(num):
        primes = []
        i = 2
        while i <= num:
            if num % i == 0:
                num = num // i
                primes.append(i)
                i = 2
            else:
                i += 1
        return tuple(primes)

    @staticmethod
    def __clarify_fraction(value):
        """returns a fractional value of an int of a float, private method"""
        if isinstance(value, int):
            return fraction(value, 1)
        if isinstance(value, float):
            return fraction.estimate_fraction(value)
        if isinstance(value, fraction):
            return value
