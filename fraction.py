import inspect
from decimal import Decimal
from math import gcd
from typing import Any, Callable, TypeVar


def staticmethod(func):
    def inner(*args):
        return func(*args)

    return inner


class fraction:
    F = TypeVar('F', bound=Callable[..., Any])

    class PrivateAttribute(Exception):
        pass

    @staticmethod
    def __clarify_args(func: F):
        """decorator to make all args in a function fraction type"""

        def inner(*args):
            args = list(args)
            for i in range(len(args)):
                if isinstance(args[i], int):
                    args[i] = fraction(i, 1)
                if isinstance(args[i], float):
                    args[i] = fraction.estimate_fraction(args[i])
            return func(*tuple(args))

        return inner

    def __init__(self, n, d=1):
        """the fractions will be simplified after initialisation"""

        # fixes string parts
        if isinstance(n, str):
            if n.isdigit():
                n = int(n)
            elif n.replace('.', '', 1).isdigit():
                n = float(n)
        if isinstance(d, str):
            if d.isdigit():
                d = int(d)
            elif d.replace('.', '', 1).isdigit():
                d = float(d)

        # fixes float parts
        if isinstance(n, float):
            n = fraction.estimate_fraction(n)
        if isinstance(d, float):
            d = fraction.estimate_fraction(d)

        # fixes fraction parts
        if isinstance(n, fraction):
            d = d * n.denominator
            n = n.numerator
        if isinstance(d, fraction):
            n = n * d.denominator
            d = d.numerator

        # if the denominator is zero the raise error
        if d == 0:
            text = "cannot create fraction with a denominator of zero (cannot divide by zero)"
            raise ZeroDivisionError(text)

        if n == 0:  # is the numerator is zero, simplify to 0/1
            self.numerator = 0
            self.denominator = 1
        else:

            if d < 0:  # if denominator is negative -> simplify
                n *= -1
                d *= -1

            hcf = gcd(n, d)  # highest common factor = greatest common denominator
            self.numerator = n // hcf  # divides both attributes by hcf
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

    @__clarify_args
    def __add__(self, other):
        """adding two fractions together"""
        n = self.numerator
        d = self.denominator
        n_ = other.numerator
        d_ = other.denominator

        result = fraction(n * d_ + n_ * d, d * d_)
        return result

    def __radd__(self, other):
        """refer to __add__"""
        return fraction.__add__(self, other)

    def __sub__(self, other):
        """subtracting two fractions from each other"""
        return self + (other * -1)

    def __rsub__(self, other):
        """refer to __sub__"""
        return other + (self * -1)

    @__clarify_args
    def __mul__(self, other):
        """multiplying fraction by fraction, int or float"""
        return fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __rmul__(self, other):
        """refer to __mul__"""
        return self.__mul__(other)

    @__clarify_args
    def __truediv__(self, other):
        """divides self by other"""
        return self * ~other

    @__clarify_args
    def __rtruediv__(self, other):
        """divides other by self"""
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

        # exponential by squaring
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
        return fraction(self.numerator + other.numerator, self.denominator + other.denominator)

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

    @__clarify_args
    def __eq__(self, other):
        """returns true is fractions are equal"""
        if self.numerator == other.numerator and self.denominator == other.denominator:
            return True
        return False

    @__clarify_args
    def __gt__(self, other):
        """returns true if first fraction is greater than the second value"""
        if self.numerator * other.denominator > self.denominator * other.numerator:
            return True
        return False

    def __lt__(self, other):
        """returns true if first fraction is less than the second value"""
        return other > self  # calls greater than and passes vars in reverse order

    @__clarify_args
    def __ge__(self, other):
        """returns true if first fraction is greater than or equal to the second value"""
        n = self.numerator
        d = self.denominator
        n_ = other.numerator
        d_ = other.denominator
        if (n == n_ and d == d_) or (n * d_ > d * n_):
            return True
        return False

    def __le__(self, other):
        """returns true if first fraction is less than or equal to the second value"""
        return other >= self  # calls greater than and passes vars in reverse order

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
    def __get_prime_factors(num: int):
        """returns the prime factors of num"""
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


class cfraction:
    F = TypeVar('F', bound=Callable[..., Any])

    @staticmethod
    def __clarify_args(func: F):
        """decorator to make all args in a function cfraction type"""

        def inner(*args):
            args = list(args)
            for i in range(len(args)):
                j = args[i]
                if isinstance(j, complex):
                    args[i] = cfraction(j, 1)
                if isinstance(j, int):
                    args[i] = cfraction(complex(j, 0), 1)
                if isinstance(j, fraction):
                    args[i] = cfraction(j.numerator, j.denominator)

            return func(*tuple(args))

        return inner

    def __init__(self, n, d):
        n = complex(n)
        d = complex(d)

        # multiples both parts of fraction by conjugate of denominator to nullify imaginary part of denominator
        n = n * d.conjugate()
        d = int((d * d.conjugate()).real)

        hcf = gcd(gcd(int(n.real), int(n.imag)), d)  # gets hcf of all numbers

        n = complex(n.real // hcf, n.imag // hcf)
        d //= hcf

        if d < 0:  # if denominator is negative -> simplify
            n *= -1
            d *= -1

        self.numerator = n
        self.denominator = d

    @property
    def real(self):
        """the real part of the fraction"""
        return fraction(self.numerator.real, self.denominator)

    @property
    def imag(self):
        """the imaginary part of the fraction"""
        return fraction(self.numerator.imag, self.denominator)

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

    def __bool__(self):
        return not self == 0

    @__clarify_args
    def __add__(self, other):
        """adding two fractions together"""
        n = self.numerator
        d = self.denominator
        n_ = other.numerator
        d_ = other.denominator

        result = cfraction(n * d_ + n_ * d, d * d_)
        return result

    def __sub__(self, other):
        return self + other * -1

    @__clarify_args
    def __mul__(self, other):
        return cfraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __pow__(self, power):  # TODO add exp by sqr
        return cfraction(self.numerator ** power, self.denominator ** power)

    def __truediv__(self, other):
        return self * ~other

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return other + self * -1

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return other * ~self

    def __and__(self, other):
        return cfraction(self.numerator + other.numerator, self.denominator + other.denominator)

    def __pos__(self):
        return self

    def __neg__(self):
        return self * -1

    def __invert__(self):
        return cfraction(self.denominator, self.numerator)

    @__clarify_args
    def __eq__(self, other):
        return complex(self.numerator.real * other.denominator, self.numerator.imag * other.denominator) == \
               complex(self.denominator * other.numerator.real, self.denominator * other.numerator.imag)

    def get_complex_value(self):
        return complex(float(self.real.get_decimal_value()), float(self.imag.get_decimal_value()))
