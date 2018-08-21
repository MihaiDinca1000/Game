import random
import sys


def gues():

    you =  int(input('guess the number: '))
    games_played = 1

    random_number = random.randint(1,9)

    if you == random_number:
        print('cool, you won!!!')
    elif you < random_number:
        print('your number is lower than the random number')
        print('the number was ',random_number)
    elif you > random_number:
        print('your number is higher that the random number')
        print('the number was ', random_number)
    else:
        print('YOU LOST')



    answer = input('Do you want to start a new game? (y for yes, any for no): ')

    if answer == 'y':
        print('New game will start')
        print('games played: ',games_played)
        games_played += 1
        gues()
    else:
        print('Wrong answer, please type Yes or No in your next attempt!')
        print('you played for ',games_played,'times')
        sys.exit(0)

gues()










# SAU !!!!

# import random
# print('type anywhere "exit" if you want to close the program')
# res = 'y'
# count = 0
#
# try:
#     while res != 'exit':
#         count += 1
#         computer_num = random.randint(1, 9)
#         user_num = input('guess the number between 1 and 9:').lower()
#         if user_num == 'exit':
#             break
#         elif int(user_num) > 9 or int(user_num) < 1:
#             print('please select between 1 and 9')
#         else:
#             user_num = int(user_num)
#             if user_num == computer_num:
#                 print('congratulations...you guessed the correct one')
#                 print('you attempted: ' + str(count) + ' times to generate output')
#             elif user_num > computer_num:
#                 print('you guessed big number than computer generated: ', computer_num)
#             else:
#                 print('you guessed small number than computer generated: ', computer_num)
#
#         res = input('enter "exit" if you want to quit: or else just enter')
#
# except ValueError:
#     print('enter proper values yaar...')








# SAU !!!!

