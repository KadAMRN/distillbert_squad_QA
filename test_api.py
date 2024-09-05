import unittest
import json
from flask_app import app  # Import the Flask app from the main API module


# Define a test case class using unittest framework to test the Flask API
class FlaskAPITestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client for the Flask app
        self.app = (
            app.test_client()
        )  # Flask provides a test client to simulate API requests
        self.app.testing = (
            True  # Enable testing mode for Flask (disables error catching)
        )

    def test_predict_success(self):
        # Test case to check the API response when both question and 
        # context are provided

        # Sample payload with a valid question and context
        payload = {
            "question": "What is quantization?",
            "context": "Quantization is a technique to reduce model size.",
        }

        # Send a POST request to the /predict endpoint with the payload as JSON
        response = self.app.post(
            "/predict",
            data=json.dumps(payload),
            content_type="application/json",
        )

        # Ensure the response is in JSON format
        self.assertEqual(response.content_type, "application/json")

        # Ensure the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the response data from JSON
        data = json.loads(response.data)

        # Verify that the 'answer' key exists in the response
        self.assertIn("answer", data)

        # Ensure the confidence score ('score') is greater than a reasonable 
        # threshold (0.2 in this case)
        self.assertGreater(data["score"], 0.1)

    def test_predict_missing_data(self):
        # Test case to handle scenarios where either the question or 
        # context is missing

        # Payload with a missing context field
        payload = {"question": "What is quantization?"}

        # Send a POST request with the incomplete payload (missing context)
        response = self.app.post(
            "/predict",
            data=json.dumps(payload),
            content_type="application/json",
        )

        # Check that the response status is 400 (Bad Request) due 
        # to missing data
        self.assertEqual(response.status_code, 400)

        # Parse the response data
        data = json.loads(response.data)

        # Check that the error message is returned in the response
        self.assertIn("error", data)


# If this script is run directly, execute the unit tests
if __name__ == "__main__":
    unittest.main()
