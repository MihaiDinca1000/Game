import math
x = 16
y = 5
print(x/y)  # afiseaza restul impartirii
print(x//y) # afiseaza rezultatul si restul nu !

d = dir() # dir contine modulele incluse in packet-ul bydefault daca ai adaugat unul va aparea si el cum e aici math
g = dir(__builtins__) # asta e unul din packet-ul pe care il contine care la randul lui contine mai multe functii, etc ...

help(pow)
help(ascii)
help(hex)

help('modules')

help(math.radians) #asa vedem o metoda din modulul math

#########################################################

#boolean variables:
w = bool(-2.345) # True
ww = bool(0)     # False
www = bool('')   # False
wwww = bool('a') # True

s = str(True) # va rezulta'True'
ss = str(False) # va rezulta'False'

i = int(True)   # ...=1
ii = int(False) # ...=0
iii = 5 + True   # ....=6
iiii = 5 * False   # ....=0

############ exemples #########################################

def volume(r):
    ''' Returns the value of a sphere with radius r.'''
    v = (4.0/3.0) * math.pi * r ** 3
    return v

print(volume(10))

#####################################
x = [12,5234, 3,234]
x.clear() # metoda clear sterge toate elementele vectorului





