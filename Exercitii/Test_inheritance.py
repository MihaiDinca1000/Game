'''
In this Python Object-Oriented Tutorial, we will be learning about inheritance and how to create subclasses.
Inheritance allows us to inherit attributes and methods from a parent class.
This is useful because we can create subclasses and get all of the functionality of our parents class,
and have the ability to overwrite or add completely new functionality without affecting the parents class in any ways.
'''

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


class Dezvoltator(Angajat):
    marire = 1.1

    def __init__(self, first, last, pay, statut):
        super().__init__(first, last, pay)
        # Angajat.__init__(self, first, last, pay) e acelasi lucru ca linia de mai sus
        self.statut = statut


class Manager(Angajat):
    def __init__(self, first, last, pay, statut, angajati = None):
        super().__init__(first, last, pay)
        if angajati is None:
            self.nr_angajati = []
        else:
            self.angajati = angajati

    def add_ang(self, ang):
        if ang not in self.angajati:
            self.angajati.append(ang)

    def remove_ang(self, ang):
        if ang in self.angajati:
            self.angajati.remove(ang)

    def print_ang(self):
        for ang in self.angajati:
            print('-->',ang.nume_Angajat())


an1 = Angajat('Sebastian', 'Bach', 67500)
dev1 = Dezvoltator('Gigi', 'Becali', 180000, 'cioban cu bani')
dev2 = Dezvoltator('viorica', 'Dancila', 26000, 'premier analfabet')

# print(help(an1)) iti arata totul despre acest angajat +mostenirea



manager1 =  Manager('Liviu', 'Dracnea', 400000, 'furacios cu in parlament', [dev2, dev1])

manager1.remove_ang(dev1)
manager1.print_ang()


# print(manger1.angajati)

# print(dev1.email)
# print(dev2.statut)


# print(dev1.pay)
# dev1.aplica_marire()
# print(dev1.pay)


