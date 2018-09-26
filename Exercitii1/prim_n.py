
def prime_number():
    num = int(input('Insert a number: '))
    a = [x for x in range(2, num) if num % x == 0]

    if num > 1:
        if len(a) == 0:
            print('your number is prime')
        else:
            print('your number is NOT prime is devided by: ',a)

prime_number()
