import random




games_count = 0
stop = False
wins = 0
while (not stop):


    you = input('Player 1: Please type your choice: rock, paper or scissors: ')

    oponent = ['rock', 'paper', 'scissors']
    choice = random.choice(oponent)
    games_count += 1

    print('the oponent choice is: ', choice)

    if choice == you:
        print('DRAW GAME')
    elif choice == 'rock' and you == 'paper':
        print('YOU LOST')
        wins -= 1
    elif choice == 'rock' and you == 'scissors':
        print('YOU WON')
        wins += 1
    elif choice == 'paper' and you == 'rock':
        print('YOU WON')
        wins += 1
    elif choice == 'paper' and you == 'scissors':
        print('YOU LOST')
        wins -= 1
    elif choice == 'scissors' and you == 'rock':
        print('YOU LOST')
        wins -= 1
    elif choice == 'scissors' and you == 'paper':
        print('YOU WON')
        wins += 1
    else:
        print('Wrong answer, please type rock, paper or scissors in your next attempt!')

    answer = input('Do you want to start a new game? (y for yes, any for no): ')

    if answer == 'y':
        print('New game will start')
        print('jocuri terminate: ',games_count)
    elif answer == 'no':
        stop = True
        print('GAME OVER')
        print('your about',wins,'times')
    else:
        print('Wrong answer, please type Yes or No in your next attempt!')
        print('you won for: ', wins, 'of',games_count,'times')
        stop = True


