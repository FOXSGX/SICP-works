# ANSWER QUESTION q1

# ANSWER QUESTION q2

# ANSWER QUESTION q3


def factorial(n):
    """Return the factorial of a non-negative integer n.

    >>> factorial(3)
    6
    >>> factorial(5)
    120
    """
    if n == 0:
        return 1
    else:
        x = 1
        acc = 1
        while x <= n:
            acc = acc * x
            x += 1
        return acc



def is_right_triangle(a, b, c):
    """Given three integers (maybe non-positive), judge whether the three
    integers can form the three sides of a right triangle.

    >>> is_right_triangle(2, 1, 3)
    False
    >>> is_right_triangle(5, -3, 4)
    False
    >>> is_right_triangle(5, 3, 4)
    True
    """
    if a <= 0 or b <= 0 or c <= 0:
        return False
    elif a**2 == b**2 + c**2 or  c**2 == a**2 + b**2 or b**2 == a**2 + c**2 :
        return True
    else:
        return False
        



def number_of_k(n, k):
    """Return the number of occurrences of k in each digit of a non-negative
    integer n.

    >>> number_of_k(999, 9)
    3
    >>> number_of_k(1234321, 2)
    2
    """
    if n == 0:
        return 1 if k == 0 else 0
    sum = 0
    while n>0:
        dig = n % 10
        if dig == k:
            sum += 1
        n = n // 10
    return sum

        
