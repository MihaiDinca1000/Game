import random

# print(dir(random))
# help(random.random)


#Display 10 random nr from the interval [0, 1)
for i in range(5):
    print(random.random())
# nr sunt intre 0 si 1


for n in range(5):
    print(random.randint(1000,10000))# include si capetele


#Generate  random nr from the interval [3, 7)
def my_random():
    return 4*random.random()+3

for i in range(4):
    print(my_random())
# este *4 ca sa fie numere intre 0 si 4
#+3 ca sa adune 0 cu 3 si 4 cu 3 =>> [3,7]


outcome = ['piatra', 'hartie', 'foarfeca']
for i in range(5):
    print(random.choice(outcome))
