from re import A

__author__ = "El Amo"

class Angajat:

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first +'.' + last + '@gmail.com'

    def nume_Angajat(self):
        return '{} {}'.format(self.first, self.last)

    # pass face sa sara peste ce avem noi de facut
    # pass

ang1 = Angajat('Sebastian', 'Bach', 60000)
ang2 = Angajat('test', 'user', 10000)


ang1.first =  'Sebastian'
ang1.last =  'Bach'
ang1.email = 'Sebastia.Bach@gmail.com'
ang1.pay = 60000

ang2.first =  'test'
ang2.last =  'user'
ang2.email = 'test.user@gmail.com'
ang2.pay = 10000

ang1.nume_Angajat()
# sau !!!
Angajat.nume_Angajat(ang1)

print(ang1.email)
print(ang2.email)

print(ang1)
print(ang2)
