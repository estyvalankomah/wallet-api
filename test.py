import unittest
import requests
from test_data import data, expected_result, update_data

class TestAPI(unittest.TestCase):
    URL = "http://localhost:5000/api/v1"

    def test_post_wallet(self):
        response = requests.post(self.URL + '/wallet', json=data)
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
        self.assertEqual(response.json()['data'], expected_result)
        print("Get wallet by ID test completed")

    def test_delete_wallet(self):
        response = requests.delete(self.URL + '/wallet/5')
        self.assertEqual(response.status_code, 200)
        print("Delete wallet test completed")

    def test_update_wallet(self):
        response = requests.put(self.URL + '/wallet/2', json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['identification_card_type'], update_data['identification_card_type'])
        self.assertEqual(response.json()['data']['identification_card_number'], update_data['identification_card_number'])
        print("Update wallet test completed")

if __name__ == "__main__":
    unittest.main()