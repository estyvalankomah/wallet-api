from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db = SQLAlchemy(app)

#Init ma
ma = Marshmallow(app)

#Wallet Class/Model
class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    other_name = db.Column(db.String(50))
    identification_card_type = db.Column(db.String(50))
    identification_card_number = db.Column(db.String(20))
    available_balance = db.Column(db.Float)
    status = db.Column(db.String(10))
    per_transaction_limit = db.Column(db.Float)

    def __init__(
        self,
        first_name,
        last_name,
        other_name,
        identification_card_type,
        identification_card_number,
        available_balance,
        status,
        per_transaction_limit):
        self.first_name = first_name
        self.last_name = last_name
        self.other_name = other_name
        self.identification_card_type = identification_card_type
        self.identification_card_number = identification_card_number
        self.available_balance = available_balance
        self.status = status
        self.per_transaction_limit = per_transaction_limit

#Wallet Schema
class WalletSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'first_name',
            'last_name',
            'other_name',
            'identification_card_type',
            'identification_card_number',
            'available_balance',
            'status',
            'per_transaction_limit')

#Init schema
wallet_schema = WalletSchema()
wallets_schema = WalletSchema(many=True)

#Create a wallet
@app.route('/wallet', methods=['POST'])
def add_wallet():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    other_name = request.json['other_name']
    identification_card_type = request.json['identification_card_type']
    identification_card_number = request.json['identification_card_number']
    available_balance = request.json['available_balance']
    status = request.json['status']
    per_transaction_limit = request.json['per_transaction_limit']

    new_wallet = Wallet(
        first_name,
        last_name,
        other_name,
        identification_card_type,
        identification_card_number,
        available_balance,
        status,
        per_transaction_limit)

    db.session.add(new_wallet)
    db.session.commit()

    return wallet_schema.jsonify(new_wallet)