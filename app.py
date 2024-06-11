from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class BankAccount:
    def __init__(self, account_number, account_holder):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = 0.0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def check_balance(self):
        return self.balance

accounts = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        account_number = request.form['account_number']
        account_holder = request.form['account_holder']
        if account_number in accounts:
            return "Account number already exists."
        accounts[account_number] = BankAccount(account_number, account_holder)
        return redirect(url_for('index'))
    return render_template('create_account.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = float(request.form['amount'])
        if account_number in accounts:
            if accounts[account_number].deposit(amount):
                return redirect(url_for('index'))
            else:
                return "Deposit amount must be positive."
        return "Account not found."
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        account_number = request.form['account_number']
        amount = float(request.form['amount'])
        if account_number in accounts:
            if accounts[account_number].withdraw(amount):
                return redirect(url_for('index'))
            else:
                return "Invalid withdraw amount."
        return "Account not found."
    return render_template('withdraw.html')

@app.route('/check_balance', methods=['GET', 'POST'])
def check_balance():
    if request.method == 'POST':
        account_number = request.form['account_number']
        if account_number in accounts:
            balance = accounts[account_number].check_balance()
            return f"Available balance: ${balance:.2f}"
        return "Account not found."
    return render_template('check_balance.html')

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')