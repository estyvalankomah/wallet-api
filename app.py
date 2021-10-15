from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from responses import ApiResponse
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
    identification_card_number = db.Column(db.String(20), unique=True)
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
@app.route('/api/v1/wallet', methods=['POST'])
def add_wallet():
    try:
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        other_name = request.json['other_name']
        identification_card_type = request.json['identification_card_type']
        identification_card_number = request.json['identification_card_number']
        available_balance = request.json['available_balance']

        acceptable_IDs = ["Ghana card", "Passport", "Voter's ID", "Driver's License"]

        if ((type(first_name) == str) and (type(last_name) == str) and (type(other_name) == str) and (type(identification_card_number) == str)):
            if(first_name and last_name and identification_card_number and available_balance):
                if identification_card_type in acceptable_IDs:
                    new_wallet = Wallet(
                        first_name,
                        last_name,
                        other_name,
                        identification_card_type,
                        identification_card_number,
                        available_balance,
                        status = "active",
                        per_transaction_limit = 1000.00)

                    db.session.add(new_wallet)
                    db.session.commit()

                    result = wallet_schema.dump(new_wallet)

                    return ApiResponse("Wallet created successfully", result, 200)
                else:
                    return ApiResponse("Invalid ID card type", {}, 417)
            else:
                return ApiResponse("Empty fields!", {}, 412)
        else:
            return ApiResponse("Invalid input!", {}, 417)

    except Exception as e:
        message = f"Missing or invalid keyword: {e.args[0]}"
        return ApiResponse(message, {}, 417)

#Get all wallets
@app.route('/api/v1/wallets', methods=['GET'])
def get_wallets():
    all_wallets = Wallet.query.all()
    result = wallets_schema.dump(all_wallets)

    if result:
        return ApiResponse("Wallets succesfully fetched", result, 200)
    else:
        return ApiResponse("No wallets exist", result, 404)


#Get single wallets
@app.route('/api/v1/wallet/<id>', methods=['GET'])
def get_wallet(id):
    wallet = Wallet.query.get(id)
    result = wallet_schema.dump(wallet)

    if wallet:
        return ApiResponse("Wallet succesfully fetched", result, 200)
    else:
        return ApiResponse("Wallet does not exist", result, 404)


#Update a wallet
@app.route('/api/v1/wallet/<id>', methods=['PUT'])
def update_wallet(id):
    wallet = Wallet.query.get(id)
    request_data = request.get_json()

    if wallet:
        for key,value in request_data.items():
            setattr(wallet, key, value)

        db.session.commit()

        return ApiResponse("Wallet updated successfully", wallet_schema.dump(wallet), 200)
    else:
        return ApiResponse("Cannot update non-existent wallet", wallet_schema.dump(wallet), 404)
   

#Delete a wallet
@app.route('/api/v1/wallet/<id>', methods=['DELETE'])
def delete_wallet(id):
    wallet = Wallet.query.get(id)

    if wallet:
        db.session.delete(wallet)
        db.session.commit()

        return ApiResponse("Wallet deleted successfully", wallet_schema.dump(wallet), 200)
    else:
        return ApiResponse("Cannot delete non-existent wallet", wallet_schema.dump(wallet), 404)


#Disable a wallet
@app.route('/api/v1/wallet/<id>/disable', methods=['PUT'])
def disable_wallet(id):
    wallet = Wallet.query.get(id)

    if wallet:
        if wallet.status == "disabled":
            return ApiResponse("Wallet already disabled", wallet_schema.dump(wallet), 400)
        else:
            wallet.status = "disabled"
            db.session.commit()

            return ApiResponse("Wallet disabled succesfully", wallet_schema.dump(wallet), 200)
    else:
        return ApiResponse("Cannot disable non-existent wallet", wallet_schema.dump(wallet), 404)

#Activate a wallet
@app.route('/api/v1/wallet/<id>/activate', methods=['PUT'])
def activate_wallet(id):
    wallet = Wallet.query.get(id)

    if wallet:
        if wallet.status == "active":
            return ApiResponse("Wallet already active", wallet_schema.dump(wallet), 400)
        else:
            wallet.status = "active"
            db.session.commit()

            return ApiResponse("Wallet activated succesfully", wallet_schema.dump(wallet), 200)
    else:
        return ApiResponse("Wallet does not exist", wallet_schema.dump(wallet), 404)

#Debit a wallet
@app.route('/api/v1/wallet/debit', methods=['PUT'])
def debit_wallet():
    id = request.json['id']
    amount = float(request.json['amount'])

    wallet = Wallet.query.get(id)

    if wallet:
        if wallet.status == "active":
            new_balance = wallet.available_balance - amount
            if new_balance >= 0:
                wallet.available_balance = new_balance
                db.session.commit()

                message = f"Wallet debited with GH {amount}"
                return ApiResponse(message, wallet_schema.dump(wallet), 200)
            else:
                return ApiResponse("You don't have enough funds to perform this transaction", wallet_schema.dump(wallet), 403)
        else:
            return ApiResponse("Cannot perform transaction on disabled wallet", wallet_schema.dump(wallet), 403)
    else:
        return ApiResponse("Cannot perform transaction on non-existent wallet", wallet_schema.dump(wallet), 404)

#Credit a wallet
@app.route('/api/v1/wallet/credit', methods=['PUT'])
def credit_wallet():
    id = request.json['id']
    amount = float(request.json['amount'])

    wallet = Wallet.query.get(id)

    if wallet:
        if wallet.status == "active":
            new_balance = wallet.available_balance + amount
            wallet.available_balance = new_balance
            
            db.session.commit()

            message = f"Wallet credited with GH {amount}"
            return ApiResponse(message, wallet_schema.dump(wallet), 200)
        else:
            return ApiResponse("Cannot perform transaction on disabled wallet", wallet_schema.dump(wallet), 403)
    else:
        return ApiResponse("Cannot perform transaction on non-existent wallet", wallet_schema.dump(wallet), 404)
    

if __name__ == '__main__':
    app.run(debug=True)