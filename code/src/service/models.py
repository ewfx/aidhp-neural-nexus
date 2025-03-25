from config import db

class DebitCardTransaction(db.Model):
    __tablename__ = 'debit_card_transactions'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String, nullable=False)
    cust_gender = db.Column(db.String, nullable=False)
    cust_account_balance = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.String, nullable=False)
    transaction_time = db.Column(db.String, nullable=False)
    transaction_amount = db.Column(db.Float, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'cust_gender': self.cust_gender,
            'cust_account_balance': self.cust_account_balance,
            'transaction_date': self.transaction_date,
            'transaction_time': self.transaction_time,
            'transaction_amount': self.transaction_amount
        }

class CreditCardTransaction(db.Model):
    __tablename__ = 'credit_card_transactions'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String, nullable=False)
    card = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    use_chip = db.Column(db.String, nullable=False)
    merchant_name = db.Column(db.String, nullable=False)
    merchant_city = db.Column(db.String, nullable=False)
    merchant_state = db.Column(db.String, nullable=False)
    zip = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.String, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'user': self.user,
            'card': self.card,
            'amount': self.amount,
            'use_chip': self.use_chip,
            'merchant_name': self.merchant_name,
            'merchant_city': self.merchant_city,
            'merchant_state': self.merchant_state,
            'zip': self.zip,
            'timestamp': self.timestamp
        }