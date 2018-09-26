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

manager1 =  Manager('Liviu', 'Dracnea', 400000, 'furacios cu in parlament', [dev2])


# print(isinstance(manager1, Manager))    # True
# print(isinstance(manager1, Angajat))    # True
# print(isinstance(manager1, Dezvoltator))    # False

print('Manager este o subclasa a lui Angajat: ',issubclass(Manager, Angajat))    # True
print('Manager este o subclasa a lui Dezvoltator: ',issubclass(Manager, Dezvoltator))    # True




