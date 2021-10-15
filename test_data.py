data = {
    "first_name": "Kwame",
    "last_name": "Afram",
    "other_name": "Abrahams",
    "identification_card_type": "Ghana card",
    "identification_card_number": "9080321",
    "available_balance": 1200.00
}

expected_result = {
    "available_balance": 200.0,
    "first_name": "Esther",
    "id": 2,
    "identification_card_number": "GH457809UC",
    "identification_card_type": "Ghana card",
    "last_name": "Ankomah",
    "other_name": "Mmra",
    "per_transaction_limit": 1000.0,
    "status": "active"
}

update_data = {
    "identification_card_type": "Passport",
    "identification_card_number": "GH 65477877",
    "available_balance": 55500.00,
    "per_transaction_limit": 10000.00
}