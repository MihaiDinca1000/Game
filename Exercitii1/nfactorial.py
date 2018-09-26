
# n = int(input('factorialul lui numarului: '))
num = 1

# while n>=1:
#     num=num*n
#     n=n-1
#     print(num)

# sau !!!


def factorial(x):
    result = 1
    for i in range(2, x + 1):
        result *= i
    return result

# print(factorial(4))

# sau !!!

def factorial1(n):
    if n < 2:
        return 1
    return n * factorial1(n - 1)

print(factorial1 (int(input('factorialul lui: '))))