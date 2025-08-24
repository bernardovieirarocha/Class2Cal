import unittest
import datetime
from cefet2ics.timetable import first_occurrence, format_dt

class TestTimetable(unittest.TestCase):
    def test_first_occurrence(self):
        start = datetime.date(2025,8,4) # Monday
        self.assertEqual(first_occurrence(start, 'MO'), start)
        self.assertEqual(first_occurrence(start, 'WE'), datetime.date(2025,8,6))
        self.assertEqual(first_occurrence(start, 'FR'), datetime.date(2025,8,8))

    def test_format_dt(self):
        d = datetime.date(2025,8,4)
        self.assertEqual(format_dt(d, '07:00'), '20250804T070000')
        self.assertEqual(format_dt(d, '22:30'), '20250804T223000')

if __name__ == '__main__':
    unittest.main()
