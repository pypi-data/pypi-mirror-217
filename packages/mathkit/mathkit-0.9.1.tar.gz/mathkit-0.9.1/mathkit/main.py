import math

def add(num1=None, num2=None):
    if num1 is None:
        num1 = int(input("Enter first number: "))
    if num2 is None:
        num2 = int(input("Enter second number: "))
    print("Your answer is", num1 + num2)

def cbrt(num=None):
    if num is None:
        num = int(input("Enter the number: "))
    cbrt = num ** (1/3)
    print("The cube root of", num, "is", cbrt)

def cube(num=None):
    if num is None:
        num = int(input("Enter the number: "))
    print("Cube of the number is", num * num * num)

def div(num1=None, num2=None):
    if num1 is None:
        num1 = int(input("Enter first number: "))
    if num2 is None:
        num2 = int(input("Enter second number: "))
    print("Your answer is", num1 / num2)

def fact(num=None):
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
            hcf = i
    print("The H.C.F. of", num1, "and", num2, "is", hcf)

def lcm(num1=None, num2=None):
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
            lcm = greater
            break
        greater += 1
    print("The LCM of", num1, "and", num2, "is", lcm)
    input("Press Enter to continue")

def log(num=None):
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
        if num == None:
            num = int(input("Enter the number: "))
        print(math.log(num))
    elif choice == 4:
        exit()
    else:
        print("Invalid choice!")
        log()

def mod(num1=None, num2=None):
    if num1 is None:
        num1 = int(input("Enter first number: "))
    if num2 is None:
        num2 = int(input("Enter second number: "))
    print("Your answer is", num1 % num2)

def mul(num1=None, num2=None):
    if num1 is None:
        num1 = int(input("Enter first number: "))
    if num2 is None:
        num2 = int(input("Enter second number: "))
    print("Product =", num1 * num2)

def per(num=None, per=None):
    print("1. Percentage of a number")
    print("2. Percentage increase")
    print("3. Percentage decrease")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        if num is None:
            num = float(input("Enter the number: "))
        elif per is None:
            per = float(input("Enter the percentage: "))
        print(str(per) + "% of " + str(num) + " is " + str((per / 100) * num))
    elif choice == 2:
        if num is None:
            num = float(input("Enter the number: "))
        elif per is None:
            per = float(input("Enter the percentage: "))
        print(str(num) + " increased by " + str(per) + "% is " + str(num + ((per / 100) * num)))
    elif choice == 3:
        if num is None:
            num = float(input("Enter the number: "))
        elif per is None:
            per = float(input("Enter the percentage: "))
        print(str(num) + " decreased by " + str(per) + "% is " + str(num - ((per / 100) * num)))
    elif choice == 4:
        exit()
    else:
        print("Invalid choice!")
        per(num)

def power(num=None):
    print("Power Of numbers")
    if num is None:
        num = int(input("Enter the number: "))
    b = int(input("Enter the power: "))
    c = num ** b
    print("The answer is:", c)


def sqrt(num=None):
    if num is None:
        num = int(input("Enter a number: "))
    print("Square root of", num, "is", num ** 0.5)

def sqr(num1=None):
    if num1 is None:
        num1 = float(input("Enter a number: "))
    print("The square of", num1, "is", num1 * num1)

def sub(num1=None, num2=None):
    if num1 is None:
        num1 = int(input("Enter first number: "))
    if num2 is None:
        num2 = int(input("Enter second number: "))
    print("Your answer is", num1 - num2)
