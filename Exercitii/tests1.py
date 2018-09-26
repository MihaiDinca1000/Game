__author__ = "El Amo"

class Angajat:

    marire = 1.04
    nr_angajati = 0

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first +'.' + last + '@gmail.com'

        Angajat.nr_angajati += 1

    def nume_Angajat(self):
        return '{} {}'.format(self.first, self.last)


    def aplica_marire(self):
        self.pay = int(self.pay * self.marire)


an1 = Angajat('Sebastian', 'Bach', 60000)
an2 = Angajat('test', 'user', 10000)




print(Angajat.nr_angajati)

# print(an1.__dict__) # afiseaza tot obiectul
# print(Angajat.__dict__) # afiseaza tot obiectul

# Angajat.marire = 1.05

# an1.marire = 1.06
# Angajat.marire(an1)
# print(an1.pay)
# print(an1.marire)

# Angajat.aplica_marire(an2)
# print(an2.pay)