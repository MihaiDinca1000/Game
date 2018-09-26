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

    @classmethod
    def regleaza_marire(cls, marirea):
        cls.marire = marirea


an1 = Angajat('Sebastian', 'Bach', 60000)
an2 = Angajat('test', 'user', 10000)

Angajat.regleaza_marire(1.05) # poti pune si an1.regleaza..... si va fi acelasi lucru

print(Angajat.marire)
print(an1.marire)
print(an2.marire)