class BankAccount:
    bank_name = "Global Bank"  # переменная класса

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient funds")

acc1 = BankAccount("Anna", 1000)
acc2 = BankAccount("John", 500)

acc1.deposit(200)
acc2.withdraw(100)

print(acc1.owner, acc1.balance)
print(acc2.owner, acc2.balance)
print(BankAccount.bank_name)
