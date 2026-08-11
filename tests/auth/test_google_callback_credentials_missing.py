"""
Unit Test Suite: Google Callback Endpoint (Missing Credentials)
===============================================================
This test file validates the '/api/auth/google/callback' endpoint when server credentials are missing.
It verifies 400 Bad Request error status codes and detail message outputs.

Strict Constraints:
- Exactly 1 TestClass per file.
- Exactly 1 self.assert* statement per test function.
"""

import sys
import os
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

# Ensure backend directory is in sys.path for importing app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from main import app


class TestGoogleCallbackCredentialsMissing(unittest.TestCase):
    """
    Test Class: TestGoogleCallbackCredentialsMissing
    -------------------------------------------------
    Description:
        Tests backend behavior when Google OAuth callback receives a request without backend client credentials configured.
    """

    def setUp(self):
        """
        Function: setUp
        ---------------
        Instantiates FastAPI TestClient instance prior to executing each test function.
        """
        self.client = TestClient(app)

    @patch("main.GOOGLE_CLIENT_ID", "")
    @patch("main.GOOGLE_CLIENT_SECRET", "")
    def test_callback_missing_credentials_status_code(self):
        """
        Function: test_callback_missing_credentials_status_code
        --------------------------------------------------------
        Description:
            Verifies that invoking callback without credentials returns an HTTP 400 Bad Request status code.
        Assertions:
            Contains 1 assertion checking status code equality.
        """
        response = self.client.get("/api/auth/google/callback?code=test_code", follow_redirects=False)
        self.assertEqual(response.status_code, 400)

    @patch("main.GOOGLE_CLIENT_ID", "")
    @patch("main.GOOGLE_CLIENT_SECRET", "")
    def test_callback_missing_credentials_detail(self):
        """
        Function: test_callback_missing_credentials_detail
        ------------------------------------------------──-
        Description:
            Verifies that invoking callback without credentials returns the expected detail error message.
        Assertions:
            Contains 1 assertion checking JSON error detail string.
        """
        response = self.client.get("/api/auth/google/callback?code=test_code", follow_redirects=False)
        self.assertEqual(response.json()["detail"], "OAuth credentials missing in server config.")


if __name__ == "__main__":
    unittest.main()
