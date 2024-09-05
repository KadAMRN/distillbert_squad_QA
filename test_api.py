import unittest
import json
from flask_app import app


class FlaskAPITestCase(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_predict_success(self):
        # Test case where question and context are provided
        payload = {
            "question": "What is quantization?",
            "context": "Quantization is a technique to reduce model size and speed up inference."
        }
        
        # Send a POST request to the API
        response = self.app.post('/predict', data=json.dumps(payload), content_type='application/json')

        # Ensure the response is JSON
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)

        # Parse the response data
        data = json.loads(response.data)
        
        # Check if 'answer' is in the response
        self.assertIn("answer", data)
        self.assertGreater(data["score"], 0.2)  # Check that the score is reasonable

    def test_predict_missing_data(self):
        # Test case where question or context is missing
        payload = {
            "question": "What is quantization?"
        }

        # Send a POST request with missing context
        response = self.app.post('/predict', data=json.dumps(payload), content_type='application/json')

        # Check for a 400 Bad Request status code
        self.assertEqual(response.status_code, 400)

        # Check for error message
        data = json.loads(response.data)
        self.assertIn("error", data)


if __name__ == '__main__':

    unittest.main()
