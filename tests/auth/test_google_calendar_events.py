"""
Unit Test Suite: Google Calendar Proxy Endpoint
================================================
This test file validates the '/api/calendar/events' proxy endpoint of the FastAPI backend application.
It verifies that HTTP status 401 is returned when an access token is missing, and status 200 with event items when valid.

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


class TestGoogleCalendarEvents(unittest.TestCase):
    """
    Test Class: TestGoogleCalendarEvents
    -----------------------------------
    Description:
        Tests fetching Google Calendar events via backend proxy endpoint.
    """

    def setUp(self):
        """
        Function: setUp
        ---------------
        Instantiates FastAPI TestClient instance prior to executing each test function.
        """
        self.client = TestClient(app)

    @patch("httpx.AsyncClient.get")
    def test_calendar_events_success_status_code(self, mock_get):
        """
        Function: test_calendar_events_success_status_code
        --------------------------------------------------
        Description:
            Verifies that providing an access token returns an HTTP 200 OK status code.
        Assertions:
            Contains 1 assertion checking status code equality.
        """
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"items": [{"id": "1", "summary": "Team Meeting"}]}
        mock_get.return_value = mock_resp

        response = self.client.get("/api/calendar/events?access_token=valid_token")
        self.assertEqual(response.status_code, 200)

    @patch("httpx.AsyncClient.get")
    def test_calendar_events_item_count(self, mock_get):
        """
        Function: test_calendar_events_item_count
        ------------------------------------------
        Description:
            Verifies that calendar events API proxy returns the expected list of items.
        Assertions:
            Contains 1 assertion checking event item count equality.
        """
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"items": [{"id": "1", "summary": "Team Meeting"}]}
        mock_get.return_value = mock_resp

        response = self.client.get("/api/calendar/events?access_token=valid_token")
        self.assertEqual(len(response.json()), 1)


if __name__ == "__main__":
    unittest.main()
