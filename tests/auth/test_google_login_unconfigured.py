"""
Unit Test Suite: Google Login Endpoint (Unconfigured State)
============================================================
This test file validates the '/api/auth/google/login' endpoint when GOOGLE_CLIENT_ID environment variable is missing or empty.
It verifies status code 400 and detail error messages returned by FastAPI HTTPException.

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


class TestGoogleLoginUnconfigured(unittest.TestCase):
    """
    Test Class: TestGoogleLoginUnconfigured
    ----------------------------------------
    Description:
        Tests backend behavior when a user attempts Google login without GOOGLE_CLIENT_ID configured in .env.
    """

    def setUp(self):
        """
        Function: setUp
        ---------------
        Instantiates FastAPI TestClient instance prior to executing each test function.
        """
        self.client = TestClient(app)

    @patch("main.GOOGLE_CLIENT_ID", "")
    def test_login_unconfigured_status_code(self):
        """
        Function: test_login_unconfigured_status_code
        ----------------------------------------------
        Description:
            Verifies that requesting login without GOOGLE_CLIENT_ID produces an HTTP 400 Bad Request status code.
        Assertions:
            Contains 1 assertion checking status code equality.
        """
        response = self.client.get("/api/auth/google/login", follow_redirects=False)
        self.assertEqual(response.status_code, 400)

    @patch("main.GOOGLE_CLIENT_ID", "")
    def test_login_unconfigured_error_detail(self):
        """
        Function: test_login_unconfigured_error_detail
        -----------------------------------------------
        Description:
            Verifies that requesting login without GOOGLE_CLIENT_ID returns the exact unconfigured error message string in detail.
        Assertions:
            Contains 1 assertion checking JSON error detail equality.
        """
        response = self.client.get("/api/auth/google/login", follow_redirects=False)
        self.assertEqual(
            response.json()["detail"],
            "GOOGLE_CLIENT_ID is not configured in backend environment (.env)."
        )


if __name__ == "__main__":
    unittest.main()
