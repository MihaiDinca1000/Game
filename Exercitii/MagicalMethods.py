''''
In this Python Object-Oriented Tutorial, we will be learning about special methods.
These are also called magic or dunder methods.
These methods allow us to emulate built-in types or implement operator overloading.
These can be extremely powerful if used correctly.
We will start by writing a few special methods of our own and then look at how some of them are used in the Standard Library.
'''

class Angajat:

    marire = 1.01


    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.email = first +'.' + last + '@gmail.com'
        self.pay = pay


    def nume_Angajat(self):
        return '{} {}'.format(self.first, self.last)

    def aplica_marire(self):
        self.pay = int(self.pay * self.marire)

    def __repr__(self):
#poate sa imi afiseze obiectul asa cum e ci nu adresa lui in memorie si fara sa folosesc __dict__
        return "Angajat('{}', '{}', {})".format(self.first, self.last, self.pay)

    def __str__(self):
#imi afiseaza obiectul fara apostroafe si nimic, daca ii dau print fara sa specific si methoda __str__
        return '{}-{}'.format(self.nume_Angajat(), self.email)


    def __add__(self, other):
#metoda care combina variabilele a 2 boecte de acelasi tip, aici am vazut cat este add de pay
        return self.pay + other.pay

    def __len__(self):
        return len(self.nume_Angajat())

an1 = Angajat('Sebastian', 'Bach', 60000)
an2 = Angajat('test', 'user', 10000)

# print(an1)

# print(repr(an1))
# print(str(an1))

#cele 2 printuri de mai sus sunt lafel ca astea 2 de mai jos:

print(an1.__repr__())
print(an1.__str__())


# print(2+3) # in spatele ei asta se intampla defapt(cand avem __func__ s.n. dunder method):
# print(int.__add__(7, 3))
# print(str.__add__('a', 'd'))

#asa se foloseste __add__(self, other)
print(an1+an2)
#Exista sia letele ca __mul__, and, or , mod,  se numesc => " Emulating numeric types"


# print(len('gigel')) # sau
# print('gigel'.__len__())

print(len(an1))