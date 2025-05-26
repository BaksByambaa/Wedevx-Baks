class BankAccount:
    def __init__(self, initial_balance):
        self.balance = float(initial_balance)
    
    def deposit(self, amount):
        self.balance += float(amount)
        print(f"Balance after depositing {self.balance}")
        
    def withdraw(self, amount):
        amount = float(amount)
        if amount > self.balance:
            print("Insufficient funds")
            print(f"Balance after withdrawing {self.balance}")
        else:
            self.balance -= amount
            print(f"Balance after withdrawing {self.balance}")
    
    def get_balance(self):
        return self.balance

initial_balance = input()
deposit_amount = input()
withdraw_amount = input()

account = BankAccount(initial_balance)
account.deposit(deposit_amount)
account.withdraw(withdraw_amount) 