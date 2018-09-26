import random
import sys

status = False
cows = 0
bulls = 0

input_number= list(input('guess the number: '))
guess_number = str(random.randint(1000,9999))
print(guess_number)


for i in range(0,4):
    if guess_number[i] == input_number[i]:
        cows += 1

    if guess_number[i] in input_number:
        bulls += 1

if len(input_number) > 4:
    print('is not a valid number')
    sys.exit(o)

print('in your number you have {} cows and  {} bulls'.format(cows, bulls))
