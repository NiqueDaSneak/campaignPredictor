import unittest
import json
from api.app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_predict(self):
        sample_data = {
            "title": "Sample Project",
            "goal": 10000.0,
            "backers": 100
        }
        response = self.app.post('/predict', data=json.dumps(sample_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('amount_raised', data)

if __name__ == '__main__':
    unittest.main()
