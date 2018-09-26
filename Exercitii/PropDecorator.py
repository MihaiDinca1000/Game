'''
In this Python Object-Oriented Tutorial, we will be learning about the property decorator.
The property decorator allows us to define Class methods that we can access like attributes.
This allows us to implement getters, setters, and deleters.
'''

class Angajat:

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    @property #getter
    def email(self):
        return '{}.{}@gmail.com'.format(self.first, self.last)

    @property #getter
    def nume_Angajat(self):
        return '{} {}'.format(self.first, self.last)

    @nume_Angajat.setter #setter
    def nume_Angajat(self, name):
        first, last = name.split(' ')
        self.first = first
        self.last = last


    @nume_Angajat.deleter #deletter
    def nume_Angajat(self):
        print('delete Nume Angajat! ->', self.first, self.last)
        self.first = None
        self.last = None

an1 = Angajat('Sebastian', 'Bach', 60000)
an2 = Angajat('George', 'Handel', 44300)

an1.first = 'Johann'
an2.nume_Angajat =  'Frederich Haendel'

# print(an1.first)
# print(an1.email)
# print(an1.nume_Angajat)

print(an2.nume_Angajat)
print(an1.nume_Angajat)


del an1.nume_Angajat

print(an1.nume_Angajat)
