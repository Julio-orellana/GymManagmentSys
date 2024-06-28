# Sistema de gestion de gimnasio con POO en Python
# Autor: Julio Orellana 2024

import os
import json
import time

# Funciones auxiliares:
def get_date():
    return time.strftime("%d-%m-%Y")

# Decoradores:
# Decorador para extender los metodos de la clase Database
def database_decorator(cls):
    class Wrapper(cls, Database):
        pass
    return Wrapper

# Clases:
class Database:
    def __init__(self):
        self.path = f"{os.path.dirname(os.path.abspath(__file__))}/{'db'}"
        self.data = {}

    def load(self, file):
        with open(f"{self.path}/{str(file)}.json", "r") as f:
            self.data = json.load(f)


class Auth(Database):
    def __init__(self):
        super().__init__()
        self.users("users", {})

    def register(self, username, password):
        if username in self.users:
            print("El usuario ya está registrado.")
            return False
        self.users[username] = password
        self.data["users"] = self.users
        self.save("users")  # Guarda los datos actualizados
        print("Usuario registrado exitosamente.")
        return True

    def login(self, username, password):
        if username not in self.users:
            print("Usuario no encontrado.")
            return False
        if self.users[username] != password:
            print("Contraseña incorrecta.")
            return False
        print("Inicio de sesión exitoso.")
        return True


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

# Se extiende la clase Database con el decorador 
@database_decorator
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

# Se extiende la clase Database con el decorador 
@database_decorator
class Gym:
    def __init__(self):
        pass