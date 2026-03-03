class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance

account = BankAccount(1000)

print(account.__balance)  # ❌ This will raise an error — it's "private"
# Lembrando que o Vinicius passou a artimanha em python pra fazer aparecer
# Não vou nem mostrar aqui para vocês não usarem pro mal
account.deposit(500)
print(account.get_balance())  # ✅ This works — access is controlled
