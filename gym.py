# Sistema de gestion de gimnasio

class Client:
    def __init__(self, name, age, membership):
        self.name = name
        self.age =  age
        self.membership = membership
    
    def add_membership(self, membership):
        self.membership = membership
    
    def add_payment(self, payment):
        self.payment = payment

class Membership:
    def __init__(self, membership_id, membership_type, price):
        self.membership = membership_id
        self.membership_type = membership_type
        self.price = price

class Payment:
    def __init__(self, id_payment, amount, date):
        self.id_payment = id_payment
        self.amount = amount
        self.date = date

class Staff:
    def __init__(self, name, age, position):
        self.name = name
        self.age = age
        self.position = position

    def create_client(self):
        self.name = input("Ingrese el nombre del cliente: ")
        self.age = input("Ingrese la edad del cliente: ")
        self.membership = input("Ingrese el tipo de membresia: ")
        if not (self.name or self.age or self.membership):
            # Si no se ingresan los datos, no se retorna un cliente
            pass
        return Client(self.name, int(self.age), self.membership)

class Gym:
    def __init__(self):
        self.members 