from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from config import app, db
from models import DebitCardTransaction, CreditCardTransaction

CORS(app)  # Enable CORS for all routes

CREDIT_CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'creditCardTransactions.csv')
DEBIT_CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'debitCardTransactions.csv')

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    if data['transactionType'] == 'credit':
        # Append to credit card transactions CSV file
        with open(CREDIT_CSV_FILE_PATH, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                data['user'],
                data['card'],
                data['amount'],
                data['useChip'],
                data['merchantName'],
                data['merchantCity'],
                data['merchantState'],
                data['zip'],
                data['timestamp']
            ])
        # Add to credit card transactions database
        new_transaction = CreditCardTransaction(
            user=data['user'],
            card=data['card'],
            amount=data['amount'],
            use_chip=data['useChip'],
            merchant_name=data['merchantName'],
            merchant_city=data['merchantCity'],
            merchant_state=data['merchantState'],
            zip=data['zip'],
            timestamp=data['timestamp']
        )
        db.session.add(new_transaction)
        db.session.commit()
    else:
        # Append to debit card transactions CSV file
        with open(DEBIT_CSV_FILE_PATH, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                data['customer_id'],
                data['cust_gender'],
                data['cust_account_balance'],
                data['transaction_date'],
                data['transaction_time'],
                data['transaction_amount']
            ])
        # Add to debit card transactions database
        new_transaction = DebitCardTransaction(
            customer_id=data['customer_id'],
            cust_gender=data['cust_gender'],
            cust_account_balance=data['cust_account_balance'],
            transaction_date=data['transaction_date'],
            transaction_time=data['transaction_time'],
            transaction_amount=data['transaction_amount']
        )
        db.session.add(new_transaction)
        db.session.commit()
    
    return jsonify({'message': 'Transaction added successfully'}), 201

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    transaction_type = request.args.get('type')
    user_id = request.args.get('user')
    transactions = []
    if transaction_type == 'credit':
        with open(CREDIT_CSV_FILE_PATH, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == user_id:
                    transactions.append({
                        'user': row[0],
                        'card': row[1],
                        'amount': row[2],
                        'useChip': row[3],
                        'merchantName': row[4],
                        'merchantCity': row[5],
                        'merchantState': row[6],
                        'zip': row[7],
                        'timestamp': row[8]
                    })
    return jsonify(transactions)

@app.route('/api/verify', methods=['GET'])
def verify():
    return jsonify({'message': 'API is working'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)