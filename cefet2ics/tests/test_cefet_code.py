import unittest
from cefet2ics.cefet_code import parse_cefet_codes

class TestCefetCode(unittest.TestCase):
    def test_valid_code(self):
        result = parse_cefet_codes('24M56')
        self.assertEqual(result[0]['days'], ['MO','WE'])
        self.assertEqual(result[0]['turn'], 'M')
        self.assertEqual(result[0]['start_slot'], 5)
        self.assertEqual(result[0]['end_slot'], 6)
        self.assertEqual(result[0]['start_time'], '10:40')
        self.assertEqual(result[0]['end_time'], '12:20')

    def test_noturno_slot_error(self):
        result = parse_cefet_codes('56N56')
        self.assertTrue('error' in result[0])

    def test_multiple_codes(self):
        result = parse_cefet_codes('24M56 3T12')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]['days'], ['TU'])
        self.assertEqual(result[1]['turn'], 'T')
        self.assertEqual(result[1]['start_slot'], 1)
        self.assertEqual(result[1]['end_slot'], 2)

    def test_invalid_code(self):
        result = parse_cefet_codes('99X99')
        self.assertTrue('error' in result[0])

if __name__ == '__main__':
    unittest.main()
