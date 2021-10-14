import unittest
import requests

class TestAPI(unittest.TestCase):
    URL = "http://localhost:5000/api/v1"

    data = {
        "first_name": "Kenneth",
        "last_name": "Lartey",
        "other_name": "Abrahams",
        "identification_card_type": "Ghana card",
        "identification_card_number": "907807580321",
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

    def test_post_wallet(self):
        response = requests.post(self.URL + '/wallet', json=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 9)
        print("Post wallet test completed")

    def test_get_all_wallets(self):
        response = requests.get(self.URL + '/wallets')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 5)
        print("Get all wallets test completed")

    def test_get_wallet(self):
        response = requests.get(self.URL + '/wallet/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data'], self.expected_result)
        print("Get wallet by ID test completed")

    def test_delete_wallet(self):
        response = requests.delete(self.URL + '/wallet/5')
        self.assertEqual(response.status_code, 200)
        print("Delete wallet test completed")

    def test_update_wallet(self):
        response = requests.put(self.URL + '/wallet/2', json=self.update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['identification_card_type'], self.update_data['identification_card_type'])
        self.assertEqual(response.json()['data']['identification_card_number'], self.update_data['identification_card_number'])
        print("Update wallet test completed")

if __name__ == "__main__":
    unittest.main()