"""
Unit Test Suite: Google Callback Endpoint (Successful Flow)
=============================================================
This test file validates the '/api/auth/google/callback' endpoint during a successful OAuth 2.0 flow.
It mocks Google token exchange & user profile endpoints and verifies 307 redirect responses to the frontend URL.

Strict Constraints:
- Exactly 1 TestClass per file.
- Exactly 1 self.assert* statement per test function.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Ensure backend directory is in sys.path for importing app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend')))

from main import app


class TestGoogleCallbackSuccess(unittest.TestCase):
    """
    Test Class: TestGoogleCallbackSuccess
    --------------------------------------
    Description:
        Tests successful Google OAuth 2.0 callback code exchange, user profile fetching, and frontend redirect response generation.
    """

    def setUp(self):
        """
        Function: setUp
        ---------------
        Instantiates FastAPI TestClient instance prior to executing each test function.
        """
        self.client = TestClient(app)

    @patch("main.GOOGLE_CLIENT_ID", "valid_client_id")
    @patch("main.GOOGLE_CLIENT_SECRET", "valid_client_secret")
    @patch("httpx.AsyncClient.post")
    @patch("httpx.AsyncClient.get")
    def test_callback_success_status_code(self, mock_get, mock_post):
        """
        Function: test_callback_success_status_code
        -------------------------------------------
        Description:
            Verifies that a valid authorization code exchange returns an HTTP 307 Temporary Redirect status code.
        Assertions:
            Contains 1 assertion checking HTTP status code equality.
        """
        mock_token_resp = MagicMock()
        mock_token_resp.status_code = 200
        mock_token_resp.json.return_value = {"access_token": "mock_access_token"}
        mock_post.return_value = mock_token_resp

        mock_userinfo_resp = MagicMock()
        mock_userinfo_resp.status_code = 200
        mock_userinfo_resp.json.return_value = {"name": "Test User", "email": "test@example.com"}
        mock_get.return_value = mock_userinfo_resp

        response = self.client.get("/api/auth/google/callback?code=valid_code", follow_redirects=False)
        self.assertEqual(response.status_code, 307)

    @patch("main.GOOGLE_CLIENT_ID", "valid_client_id")
    @patch("main.GOOGLE_CLIENT_SECRET", "valid_client_secret")
    @patch("httpx.AsyncClient.post")
    @patch("httpx.AsyncClient.get")
    def test_callback_success_redirect_location(self, mock_get, mock_post):
        """
        Function: test_callback_success_redirect_location
        -------------------------------------------------
        Description:
            Verifies that the redirect Location header contains the encoded 'user=' parameter string destined for the frontend.
        Assertions:
            Contains 1 assertion checking inclusion of substring in response Location header.
        """
        mock_token_resp = MagicMock()
        mock_token_resp.status_code = 200
        mock_token_resp.json.return_value = {"access_token": "mock_access_token"}
        mock_post.return_value = mock_token_resp

        mock_userinfo_resp = MagicMock()
        mock_userinfo_resp.status_code = 200
        mock_userinfo_resp.json.return_value = {"name": "Test User", "email": "test@example.com"}
        mock_get.return_value = mock_userinfo_resp

        response = self.client.get("/api/auth/google/callback?code=valid_code", follow_redirects=False)
        self.assertIn("user=", response.headers["location"])


if __name__ == "__main__":
    unittest.main()
