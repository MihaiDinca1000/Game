################## FIBONACCI RECURSIV ########################################################

def fibonacci3(n):
    if n == 1:
        return 1
    elif n == 2:
        return 1
    elif n > 2:
        return fibonacci3(n-1) + fibonacci3(n-2)

# print(fibonacci3(10))

# for n in range(1, 101):
#     print(n, ":", fibonacci3(n))
# pentru numere mari asta va compila forate greu pentru ca el va face asa:
# ex: fibonacci3(10)= fibonacci3(9)+fibonacci3(8)+fibonacci3(7)+ ....
# si fibonacci3(9) lafel !!!

####################################################################################################

# Memoization: idea-->> cache values v1

fibonacci_cache = {}

def fibonacci1(n):
    #if we have cached the value, then return it
    if n in fibonacci_cache:
        return fibonacci_cache[n]

    #compute the Nth term
    if n == 1:
        value =1
    elif n == 2:
        value = 1
    elif n > 2:
        value  = fibonacci1(n-1) + fibonacci1(n-2)

    #Cache the value and return it
    fibonacci_cache[n] = value
    return value

# for n in range(1, 101):
#     print(n, ":", fibonacci1(n))

####################################################################################################
# Memoization: idea-->> cache values v2 !!! si cea mai buna

from functools import lru_cache

@lru_cache(maxsize=1000)
def fibonacci3(n):
    if n == 1:
        return 1
    elif n == 2:
        return 1
    elif n > 2:
        return fibonacci3(n-1) + fibonacci3(n-2)

# for n in range(1, 201):
#     print(n, ":", fibonacci1(n))



######################################################################################################

@lru_cache(maxsize=1000)
def fibonacci3(n):
# check the input is an integer
    if type(n) != int:
        raise TypeError("n must be a positive int")
    if n<1:
        raise ValueError("n must be a positive int")

    # Compute the Nth term:
    if n == 1:
        return 1
    elif n == 2:
        return 1
    elif n > 2:
        return fibonacci3(n-1) + fibonacci3(n-2)

print(fibonacci3(-3))