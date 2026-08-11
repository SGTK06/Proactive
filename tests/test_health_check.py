"""
Unit Test Suite: Root Health Check Endpoint
===========================================
This test file validates the root health check endpoint ('/') of the FastAPI backend application.
It verifies both HTTP status code responses and response JSON dictionary body contents.

Strict Constraints:
- Exactly 1 TestClass per file.
- Exactly 1 self.assert* statement per test function.
"""

import sys
import os
import unittest
from fastapi.testclient import TestClient

# Ensure backend directory is in sys.path for importing app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from main import app


class TestHealthCheck(unittest.TestCase):
    """
    Test Class: TestHealthCheck
    ---------------------------
    Description:
        Tests the availability, responsiveness, and exact payload output of the root '/' health check endpoint.
    """

    def setUp(self):
        """
        Function: setUp
        ---------------
        Instantiates FastAPI TestClient instance prior to executing each test function.
        """
        self.client = TestClient(app)

    def test_root_status_code(self):
        """
        Function: test_root_status_code
        -------------------------------
        Description:
            Verifies that a GET request to root '/' returns an HTTP 200 OK status code.
        Assertions:
            Contains 1 assertion checking HTTP status code equality.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_root_response_message(self):
        """
        Function: test_root_response_message
        ------------------------------------
        Description:
            Verifies that a GET request to root '/' returns the expected JSON message dictionary payload.
        Assertions:
            Contains 1 assertion checking JSON dictionary payload equality.
        """
        response = self.client.get("/")
        self.assertEqual(response.json(), {"message": "Proactive Auth Backend API is running"})


if __name__ == "__main__":
    unittest.main()
