"""
Unit Test Suite: Google Login Endpoint (Configured State)
==========================================================
This test file validates the '/api/auth/google/login' endpoint when GOOGLE_CLIENT_ID is properly configured.
It verifies 307 Temporary Redirect HTTP responses and URL location header formats.

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


class TestGoogleLoginConfigured(unittest.TestCase):
    """
    Test Class: TestGoogleLoginConfigured
    --------------------------------------
    Description:
        Tests backend behavior when a user triggers Google login with valid GOOGLE_CLIENT_ID settings.
    """

    def setUp(self):
        """
        Function: setUp
        ---------------
        Instantiates FastAPI TestClient instance prior to executing each test function.
        """
        self.client = TestClient(app)

    @patch("main.GOOGLE_CLIENT_ID", "valid_client_id_123")
    def test_login_redirect_status_code(self):
        """
        Function: test_login_redirect_status_code
        -----------------------------------------
        Description:
            Verifies that triggering Google login returns an HTTP 307 Temporary Redirect status code.
        Assertions:
            Contains 1 assertion checking status code equality.
        """
        response = self.client.get("/api/auth/google/login", follow_redirects=False)
        self.assertEqual(response.status_code, 307)

    @patch("main.GOOGLE_CLIENT_ID", "valid_client_id_123")
    def test_login_redirect_target(self):
        """
        Function: test_login_redirect_target
        -------------------------------------
        Description:
            Verifies that the HTTP Location response header correctly targets Google's OAuth 2.0 authorization URL.
        Assertions:
            Contains 1 assertion evaluating string prefix match on Location header.
        """
        response = self.client.get("/api/auth/google/login", follow_redirects=False)
        self.assertTrue(response.headers["location"].startswith("https://accounts.google.com/o/oauth2/v2/auth"))


if __name__ == "__main__":
    unittest.main()
