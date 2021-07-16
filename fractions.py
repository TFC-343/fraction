from decimal import Decimal

class fraction:
    def __init__(self, n, d):
        self.n = n  # numerator
        self.d = d  # denominator

    def __str__(self):
        n = self.numerator()
        d = self.denominator()

        return f"{n}/{d}"

    def __add__(self, other):
        """adding two fractions together"""
        n = self.n
        d = self.d
        n_ = other.n
        d_ = other.d

        new_self = fraction(n*d_, d*d_)
        new_other = fraction(d*n_, d_*n_)
        result = fraction(new_self.n + new_other.n, new_self.d)
        return result

    def __sub__(self, other):
        """subtracting two fractions from each other"""
        return self + (other*-1)

    def __mul__(self, other):
        if isinstance(other, int):
            other = fraction(other, 1)
        n = self.n
        d = self.d
        n_ = other.n
        d_ = other.d
        return fraction(n*n_, d*d_)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = fraction(other, 1)
        return self * ~other

    def __rtruediv__(self, other):
        if isinstance(other, int):
            other = fraction(other, 1)
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
        if isinstance(other, int):
            other = fraction(other, 1)
        n = self.n
        d = self.d
        n_ = other.n
        d_ = other.d
        return fraction(n+n_, d+d_)

    def __abs__(self):
        """returns float value of fraction"""
        return self.get_true_value()

    def __invert__(self):
        """equivalent to 1/'self'"""
        n = self.n
        d = self.d

        return fraction(d, n)

    def numerator(self):
        """returns the numerator of a fraction"""
        return self.simplify(r=True).n

    def denominator(self):
        """returns the denominator of a fraction"""
        return self.simplify(r=True).d

    def get_true_value(self):
        """return true value in float"""
        n = self.n
        d = self.d
        return Decimal(n) / Decimal(d)

    def simplify(self, r=False):
        """simplifies the equation"""
        n = self.n
        d = self.d

        negative = 1
        if (n < 0) ^ (d < 0):
            negative = -1
        n, d = abs(n), abs(d)

        hcf = fraction.__hcf(n, d)
        if r:
            return fraction(n // hcf * negative, d // hcf)
        self.n = n // hcf * negative
        self.d = d // hcf

    @staticmethod
    def __hcf(a, b):
        """returns highest common factor, private method"""
        rt = 1
        i = 1
        c = a if a < b else b
        jump = 2
        while i < c:
            # i need only be a prime number
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
    def __lcm(a, b):  # inefficient but unused
        """returns lowest common multiple, private method"""
        rt = 1
        i = 1
        while not(a == 1 and b == 1):
            i += 1
            if a % i == 0 and b % i == 0:
                a = a // i
                b = b // i
                rt *= i
                i = 1
            elif a % i == 0:
                a = a // i
                rt *= i
                i = 1
            elif b % i == 0:
                b = b // i
                rt *= i
                i = 1
        return rt

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
