"""
    Add two numbers and print the result.

    Args:
        num1 (int or float): The first number (default: None).
        num2 (int or float): The second number (default: None).

    Returns:
        None

"""
import math
import sys

def add(num1=None, num2=None):
    """
    Add two numbers and print the result.

    Args:
        num1 (int or float): The first number (default: None).
        num2 (int or float): The second number (default: None).

    Returns:
        None

    """
    if num1 is None:
        num1 = int(input("Enter first number: "))
    if num2 is None:
        num2 = int(input("Enter second number: "))
    print("Your answer is", num1 + num2)

def cbrt(num=None):
    """
    Calculate the cube root of a number and print the result.

    Args:
        num (int or float): The number to calculate the cube root of (default: None).

    Returns:
        None

    """
    if num is None:
        num = int(input("Enter the number: "))
    cube_root = num ** (1/3)
    print("The cube root of", num, "is", cube_root)

def cube(num=None):
    """
    Calculate the cube of a number and print the result.

    Args:
        num (int or float): The number to calculate the cube of (default: None).

    Returns:
        None

    """
    if num is None:
        num = int(input("Enter the number: "))
    print("Cube of the number is", num * num * num)

def div(num1=None, num2=None):
    """
    Divide two numbers and print the result.

    Args:
        num1 (int or float): The numerator (default: None).
        num2 (int or float): The denominator (default: None).

    Returns:
        None

    """
    if num1 is None:
        num1 = int(input("Enter first number: "))
    if num2 is None:
        num2 = int(input("Enter second number: "))
    print("Your answer is", num1 / num2)

def fact(num=None):
    """
    Calculate the factorial of a number and print the result.

    Args:
        num (int): The number to calculate the factorial of (default: None).

    Returns:
        None

    """
    if num is None:
        num = int(input("Enter the number: "))
    factorial = 1
    if num < 0:
        print("Sorry, factorial does not exist for negative numbers")
    elif num == 0:
        print("The factorial of 0 is 1")
    else:
        for i in range(1, num + 1):
            factorial = factorial * i
        print("The factorial of", num, "is", factorial)

def hcf(num1=None, num2=None):
    """
    Calculate the highest common factor (HCF) of two numbers and print the result.

    Args:
        num1 (int): The first number (default: None).
        num2 (int): The second number (default: None).

    Returns:
        None

    """
    print("HCF of two numbers")
    if num1 is None:
        num1 = int(input("Enter the first number: "))
    if num2 is None:
        num2 = int(input("Enter the second number: "))
    if num1 > num2:
        smaller = num2
    else:
        smaller = num1
    for i in range(1, smaller + 1):
        if (num1 % i == 0) and (num2 % i == 0):
            hcf_value = i
    print("The H.C.F. of", num1, "and", num2, "is", hcf_value)

def lcm(num1=None, num2=None):
    """
    Calculate the least common multiple (LCM) of two numbers and print the result.

    Args:
        num1 (int): The first number (default: None).
        num2 (int): The second number (default: None).

    Returns:
        None

    """
    print("LCM of two numbers")
    if num1 is None:
        num1 = int(input("Enter the first number: "))
    if num2 is None:
        num2 = int(input("Enter the second number: "))
    if num1 > num2:
        greater = num1
    else:
        greater = num2
    while True:
        if (greater % num1 == 0) and (greater % num2 == 0):
            lcm_value = greater
            break
        greater += 1
    print("The LCM of", num1, "and", num2, "is", lcm_value)
    input("Press Enter to continue")

def log(num=None):
    """
    Calculate the logarithm of a number and print the result.

    Args:
        num (int or float): The number to calculate the logarithm of (default: None).

    Returns:
        None

    """
    print("Logarithm")
    print("1. Logarithm of 2")
    print("2. Logarithm of 10")
    print("3. Logarithm of any number")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        print(math.log(2))
    elif choice == 2:
        print(math.log(10))
    elif choice == 3:
        if num is None:
            num = int(input("Enter the number: "))
        print(math.log(num))
    elif choice == 4:
        sys.exit()
    else:
        print("Invalid choice!")
        log()

def mod(num1=None, num2=None):
    """
    Calculate the modulus of two numbers and print the result.

    Args:
        num1 (int or float): The first number (default: None).
        num2 (int or float): The second number (default: None).

    Returns:
        None

    """
    if num1 is None:
        num1 = int(input("Enter first number: "))
    if num2 is None:
        num2 = int(input("Enter second number: "))
    print("Your answer is", num1 % num2)

def mul(num1=None, num2=None):
    """
    Multiply two numbers and print the result.

    Args:
        num1 (int or float): The first number (default: None).
        num2 (int or float): The second number (default: None).

    Returns:
        None

    """
    if num1 is None:
        num1 = int(input("Enter first number: "))
    if num2 is None:
        num2 = int(input("Enter second number: "))
    print("Product =", num1 * num2)

def percentage(num=None, perc=None):
    """
    Perform percentage calculations and print the result.

    Args:
        num (float): The number for percentage calculation (default: None).
        perc (float): The percentage value (default: None).

    Returns:
        None

    """
    print("1. Percentage of a number")
    print("2. Percentage increase")
    print("3. Percentage decrease")
    print("4. Exit")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        if num is None:
            num = float(input("Enter the number: "))
        if perc is None:
            perc = float(input("Enter the percentage: "))
        if perc is not None and num is not None:
            result = (perc / 100) * num
            print(str(perc) + "% of " + str(num) + " is " + str(result))
    elif choice == 2:
        if num is None:
            num = float(input("Enter the number: "))
        if perc is None:
            perc = float(input("Enter the percentage: "))
        if perc is not None and num is not None:
            result = num + (perc / 100) * num
            print(str(num) + " increased by " + str(perc) + "% is " + str(result))
    elif choice == 3:
        if num is None:
            num = float(input("Enter the number: "))
        if perc is None:
            perc = float(input("Enter the percentage: "))
        if perc is not None and num is not None:
            result = num - (perc / 100) * num
            print(str(num) + " decreased by " + str(perc) + "% is " + str(result))
    elif choice == 4:
        sys.exit()
    else:
        print("Invalid choice!")

    percentage()

def power(num=None):
    """
    Calculate the power of a number and print the result.

    Args:
        num (int or float): The number (default: None).

    Returns:
        None

    """
    print("Power Of numbers")
    if num is None:
        num = int(input("Enter the number: "))
    b = int(input("Enter the power: "))
    c = num ** b
    print("The answer is:", c)


def sqrt(num=None):
    """
    Calculate the square root of a number and print the result.

    Args:
        num (int or float): The number to calculate the square root of (default: None).

    Returns:
        None

    """
    if num is None:
        num = int(input("Enter a number: "))
    print("Square root of", num, "is", num ** 0.5)


def sqr(num1=None):
    """
    Calculate the square of a number and print the result.

    Args:
        num1 (int or float): The number to calculate the square of (default: None).

    Returns:
        None

    """
    if num1 is None:
        num1 = float(input("Enter a number: "))
    print("The square of", num1, "is", num1 * num1)


def sub(num1=None, num2=None):
    """
    Subtract two numbers and print the result.

    Args:
        num1 (int or float): The first number (default: None).
        num2 (int or float): The second number (default: None).

    Returns:
        None

    """
    if num1 is None:
        num1 = int(input("Enter first number: "))
    if num2 is None:
        num2 = int(input("Enter second number: "))
    print("Your answer is", num1 - num2)


def trig(num=None):
    """
    Perform trigonometric calculations (sine, cosine, tangent) for a number and print the result.

    Args:
        num (float): The number to perform trigonometric calculations on (default: None).

    Returns:
        None

    """
    print("Trigonometry")
    print("1. Sine")
    print("2. Cosine")
    print("3. Tangent")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        if num is None:
            num = float(input("Enter the number: "))
        print("Sine of", num, "is", math.sin(num))
    elif choice == 2:
        if num is None:
            num = float(input("Enter the number: "))
        print("Cosine of", num, "is", math.cos(num))
    elif choice == 3:
        if num is None:
            num = float(input("Enter the number: "))
        print("Tangent of", num, "is", math.tan(num))
    elif choice == 4:
        exit()
    else:
        print("Invalid choice!")
        trig(num)
