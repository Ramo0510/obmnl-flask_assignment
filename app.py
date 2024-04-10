# Import libraries
from flask import Flask, redirect, request, render_template, url_for
from math import ceil

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]


# Définissez une fonction pour diviser la liste des transactions en groupes de 8
def paginate_transactions(transactions, page_number):
    transactions_per_page = 8
    start_index = (page_number - 1) * transactions_per_page
    end_index = start_index + transactions_per_page
    return transactions[start_index:end_index]

# Read operation: List all transactions
@app.route("/")
def get_transactions():
    page_number = int(request.args.get('page', 1))
    total_pages = ceil(len(transactions) / 8)
    current_transactions = paginate_transactions(transactions, page_number)
    return render_template("transactions.html", transactions=current_transactions, total_balance=total_balance(), total_transactions=len(transactions), total_pages=total_pages, current_page=page_number)
    return render_template("transactions.html", transactions=transactions, total_balance=total_balance())


# Create operation: Display add transaction form
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        # Append the new transaction to the list
        transactions.append(transaction)

        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))
    
    # Render the form template to display the add transaction form
    return render_template("form.html")

# Update operation: Display edit transaction form
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']
        amount = float(request.form['amount'])

        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break

        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))
    
    # Find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

# Delete operation: Delete a transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break

    # Redirect to the transactions list page
    return redirect(url_for("get_transactions"))

# Définissez la route pour le total balance
@app.route("/balance")
def total_balance():
    # Calculez le total balance en sommant les montants de toutes les transactions
    total = sum(t["amount"] for t in transactions)
    # Retournez le total balance sous forme de chaîne de caractères
    return "Total Balance: {}".format(total)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
    