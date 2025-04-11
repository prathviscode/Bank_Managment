import random
import json


class Bank():
    Bname = "SBI Bank"

    def __init__(self):
        self.clients = []
        self.load_clients_from_file()


    def updateUser(self,client):
        self.clients.append(client)


    def authenticate(self, name, account_number, password):
        auth = False
        for i in self.clients:
            if (i.account["name"] == name and
                i.account["accno"] == account_number and
                i.account["password"] == password):
                auth = True
                return i
        print("Wrong Credentials")
        return False


    def load_clients_from_file(self):
        try:
            with open("data.json", "r") as f:
                client_list = json.load(f)
                for acc in client_list:
                    client = Client.from_dict(acc)
                    self.clients.append(client)
        except FileNotFoundError:
            pass

    def save_clients_to_file(self):
        client_list = [c.account for c in self.clients]
        with open("data.json", "w") as f:
            json.dump(client_list, f, indent=4)
class Client():

    def __init__(self,name, deposit, password, accno=None):
        self.account = {
            "name": name,
            "deposit": deposit,
            "password": password,
            "accno": accno if accno is not None else random.randint(100000, 999999)
        }
        if not accno:
            print(f"Your account has been created, account number is: {self.account['accno']}")

    @staticmethod
    def from_dict(data):
        return Client(
            name=data["name"],
            deposit=data["deposit"],
            password=data["password"],
            accno=data["accno"]
        )

    def deposit(self,amnt):
        self.account["deposit"] += amnt
        print("Deposit successful")

    def withdraw(self, amnt):
        if self.account["deposit"] >= amnt:
            self.account["deposit"] -= amnt
            print("Withdraw successful")
        else:
            print("insuffecient balance")

    def Check(self):
        print(f"Balance is: {self.account["deposit"]} rupees")





def main():
    bank = Bank()
    print(f"Hello and welcome to {bank.Bname}")
    run = True
    while run:
        print("""what would you like to do?
                            1.) Create a new Account: 
                            2.) Inquire existing account: 
                            3.) Exit: """)
        choise = int(input("press 1,2,3: "))
        if choise == 1:
            name = input("Enter name: ")
            deposit = int(input("Enter deposit amount: "))
            password = input("Enter password: ")
            client = Client(name, deposit, password)
            bank.updateUser(client)
            bank.save_clients_to_file()
        elif choise == 2:
            name = input("Enter name: ")
            account_number = int(input("Enter Account number: "))
            password = input("Enter password: ")
            current_client = bank.authenticate(name, account_number, password)
            if current_client:
                while True:
                    print("""What would you like to do: 
                                            1.) Deposit
                                            2.) Withdraw
                                            3.) Check Balance
                                            4.) Exit""")
                    choise = int(input("press 1,2,3 Or 4: "))
                    if choise == 1:
                        amount = int(input("Enter deposit amuont: "))
                        current_client.deposit(amount)
                        bank.save_clients_to_file()

                    elif choise == 2:
                        amount = int(input("Enter your withdrawal amount: "))
                        current_client.withdraw(amount)
                        bank.save_clients_to_file()

                    elif choise == 3:
                        current_client.Check()


                    else:
                        print("Thank you for visiting!")
                        break
                else:
                    print("Invalid choise")

            else:
                print("Authentication Failed!")
        else:
            bank.save_clients_to_file()
            run = False

    print("thank you")
    print("Bye")




main()
