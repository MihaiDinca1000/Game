'''
Program that shows if your number that you get is odd or even
'''

def type_number():
    n = int(input('verifie your number: '))
    if n % 2 != 0:
        return '{}: is an odd number'.format(n)
    else:
        return '{}: is an even number'.format(n)

type_number()