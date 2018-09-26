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


an_1str = 'George-Enescu-80000'
an_2str = 'Andrew-Jackson-76000'
an_3str = 'Traian-Basescu-2000'

first, last, pay = an_1str.split('-')
new_an1 = Angajat(first, last, pay)
print(new_an1.__dict__)