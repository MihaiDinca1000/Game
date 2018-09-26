import random

def f_and_l():
    a = random.sample(range(100), 10)
    print(a)
    print(a[0],a[-1])

f_and_l()