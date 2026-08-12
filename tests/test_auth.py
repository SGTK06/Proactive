import json
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from urllib.parse import parse_qs, unquote, urlparse

from fastapi.testclient import TestClient

from backend import main


class AuthApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(main.app)

    def test_health_check(self):
        response = self.client.get("/")

        self.assertEqual(response.json(), {"message": "Proactive Auth Backend API is running"})

    def test_google_login_requires_client_id(self):
        with patch.object(main, "GOOGLE_CLIENT_ID", ""):
            response = self.client.get("/api/auth/google/login", follow_redirects=False)

        self.assertEqual(response.status_code, 400)

    def test_google_login_redirects_to_google(self):
        with patch.object(main, "GOOGLE_CLIENT_ID", "client-id"):
            response = self.client.get("/api/auth/google/login", follow_redirects=False)

        location = response.headers["location"]
        parsed = urlparse(location)
        query = parse_qs(parsed.query)

        self.assertEqual(response.status_code, 307)
        self.assertEqual(parsed.netloc, "accounts.google.com")
        self.assertEqual(query["client_id"], ["client-id"])
        self.assertEqual(query["scope"], ["openid email profile"])

    def test_google_callback_requires_credentials(self):
        with patch.object(main, "GOOGLE_CLIENT_ID", ""), patch.object(main, "GOOGLE_CLIENT_SECRET", ""):
            response = self.client.get("/api/auth/google/callback?code=oauth-code", follow_redirects=False)

        self.assertEqual(response.status_code, 400)

    def test_google_callback_redirects_with_user_profile(self):
        token_response = MagicMock(status_code=200)
        token_response.json.return_value = {"access_token": "access-token"}
        userinfo_response = MagicMock(status_code=200)
        userinfo_response.json.return_value = {"name": "Alex Doe", "email": "alex@example.com"}

        async_client = MagicMock()
        async_client.__aenter__ = AsyncMock(return_value=async_client)
        async_client.__aexit__ = AsyncMock(return_value=None)
        async_client.post = AsyncMock(return_value=token_response)
        async_client.get = AsyncMock(return_value=userinfo_response)

        with (
            patch.object(main, "GOOGLE_CLIENT_ID", "client-id"),
            patch.object(main, "GOOGLE_CLIENT_SECRET", "client-secret"),
            patch.object(main.httpx, "AsyncClient", return_value=async_client),
        ):
            response = self.client.get("/api/auth/google/callback?code=oauth-code", follow_redirects=False)

        parsed = urlparse(response.headers["location"])
        user = json.loads(unquote(parse_qs(parsed.query)["user"][0]))

        self.assertEqual(response.status_code, 307)
        self.assertEqual(user, {"name": "Alex Doe", "email": "alex@example.com"})


if __name__ == "__main__":
    unittest.main()
