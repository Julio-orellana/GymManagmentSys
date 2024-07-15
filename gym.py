# Sistema de gestion de gimnasio con POO en Python
# Autor: Julio Orellana 2024

import os
import json
import time
import uuid
import pandas as pd

# Funciones auxiliares:
# Funcion para obtener la fecha actual
def get_date():
    return time.strftime("%d-%m-%Y")

# Funcion para generar un id unico 
def uuid_generator():
    return str(uuid.uuid4())

# Funcion para limpiar la pantalla
def clear_console():
    return os.system("cls" if os.name == "nt" else "clear")

# Funcion para pausar la ejecucion del programa por un tiempo determinado
def sleep(seconds):
    return time.sleep(seconds)

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
    def __init__(self, balance, due_balance, credit_card=None):
        self.balance = balance
        self.due_balance = due_balance
        self.date = get_date()
        self.payment_id
        self.credit_card = credit_card
        self.rate = 0.18

    def pay(self):
        payment_type = self.get_payment_type()
        sleep(3)
        if self.validate_payment(payment_type):
            clear_console()
            self.payment_id = uuid_generator()
            print(f"Pago realizado exitosamente.\nNumero de autorizacion: {self.payment_id}")
            return True
        clear_console()
        print("Error al realizar el pago.")
        return False
    
    def validate_payment(self, payment_type):
        match payment_type:
            case "efectivo":
                cash = int(input("Ingrese el monto en efectivo: "))
                if cash >= self.due_balance:
                    print("Transaccion Autorizada.")
                    return True              
                print("Transaccion Denegada.")
                return False

            case "credito":
                if self.balance >= self.due_balance:
                    print("Transaccion Autorizada.")
                    self.balance -= self.due_balance
                    return True
                print("Transaccion Denegada.")
                return False
            
            case "tarjeta":
                if self.validate_credit_card(self.credit_card):
                    print("Transaccion Autorizada.")
                    return True
                print("Transaccion Denegada.")
                return False
            
        return False
    
    def get_payment_type(self):
        print("Seleccione el metodo de pago: ")
        print("1. Efectivo")
        print("2. Balance de la cuenta")
        print("3. Tarjeta")
        choice = input("Seleccione una opcion: ").lower()
        while choice != "q":
            match choice:
                case "1":
                    return "efectivo"
                case "2":
                    return "credito"
                case "3":
                    return "tarjeta"
                case "q":
                    print("Saliendo...")
                    sleep(2)
                    return None
                case _:
                    print("Opcion invalida, intente de nuevo.")
        return None

    def validate_credit_card(self, credit_card):
        digits = [int(digit) for digit in str(credit_card)]
        for i in range(len(digits) -2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        return sum(digits) % 10 == 0
    
    def due_payment(self):
        return self.due_balance
    
    def interest(self, days):
        months = days / 30
        for month in range(int(months)):
            self.due_balance += self.due_balance * self.rate
        return self.due_balance
    
    def _due_payments_info(self):
        print("Generando reporte de pagos pendientes...")
        sleep(5)

        data = Database.load("data.json")
        names = []
        due_balances = []

        for role in data["members"].values():
            names.extend(role['name'])
            due_balances.extend(role['due_balance'])

        due_table = {"Miembro": names, "Saldo Pendiente": due_balances}
        df = pd.DataFrame(due_table)
        choice = str()
        
        while choice != "q":
            print("Para visualizar el reporte presione V, para exportarlo a un archivo excel presione E, o presione Q para salir.")
            choice = input("Seleccione una opcion:[v/e]: \n").lower()
            match choice:
                case "v":
                    print(df)
                case "e":
                    df.to_excel("pagos_pendientes.xlsx", index=False)
                    sleep(2)
                    print("Reporte exportado exitosamente.")
                case "q":
                    print("Saliendo...")
                    sleep(2)
                case _:
                    print("Opcion invalida, intente de nuevo.")
        return
            

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