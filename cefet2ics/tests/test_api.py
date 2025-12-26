from fastapi.testclient import TestClient
from web.main import app
import unittest
import json
from cefet2ics.models import Course, Semester
from datetime import date

client = TestClient(app)

class TestWebAPI(unittest.TestCase):
    def test_read_main(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_generate_ics(self):
        payload = {
            "semester": {
                "start_date": "2025-08-01",
                "end_date": "2025-12-01",
                "calendar_name": "Test Cal"
            },
            "courses": [
                {
                    "alias": "TEST",
                    "full_name": "Test Course",
                    "schedule_codes": "24M12"
                }
            ]
        }
        response = client.post("/api/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.startswith(b"BEGIN:VCALENDAR"))
        self.assertIn(b"SUMMARY:TEST", response.content)

if __name__ == '__main__':
    unittest.main()
