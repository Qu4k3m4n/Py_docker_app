import unittest
import requests

class TestKeyValueAPI(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8080/api/keyvalue'
        self.headers = {'Content-Type': 'application/json'}

    def test_create_key_value(self):
        data = {"key": "123", "value": "test"}
        response = requests.post(self.url, json=data, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Создано"})

        # Повторная попытка создания ключ-значение
        response = requests.post(self.url, json=data, headers=self.headers)
        self.assertEqual(response.status_code, 208)
        self.assertEqual(response.json(), {"error": "Ключ-значение уже существует"})

        # Запрос на получение созданного ключ-значение
        response = requests.get(f"{self.url}/123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"123": "test"})

        # Запрос на изменение значения ключ-значение
        response = requests.put(f"{self.url}/123", json={"value": "updated_value"}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Изменено"})

        # Запрос на получение измененного ключ-значение
        response = requests.get(f"{self.url}/123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"123": "updated_value"})

if __name__ == '__main__':
    unittest.main()
