__author__ = "El Amo"


class Angajat:
    marire = 1.04
    nr_angajati = 0

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@gmail.com'

        Angajat.nr_angajati += 1

    def nume_Angajat(self):
        return '{} {}'.format(self.first, self.last)

    def aplica_marire(self):
        self.pay = int(self.pay * self.marire)

    @classmethod
    def regleaza_marire(cls, marirea):
        cls.marire = marirea

    @classmethod
    def from_string_to_Angajat(cls, an_str):
        first, last, pay = an_str.split('-')
        return cls(first, last, pay)


an1 = Angajat('Sebastian', 'Bach', 60000)
an2 = Angajat('test', 'user', 10000)

an_1str = 'George-Enescu-80000'
an_2str = 'Andrew-Jackson-76000'
an_3str = 'Traian-Basescu-2000'

an_new2 = Angajat.from_string_to_Angajat(an_2str)



print(an_new2.__dict__)