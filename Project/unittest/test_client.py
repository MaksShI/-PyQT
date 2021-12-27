import unittest

import socket
import sys
import json
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message
from client import create_presence, process_ans


class TestSalary(unittest.TestCase):
    def test_create_presence(self):
        self.assertIsNotNone(create_presence())

    def test_create_is_presence(self):
        self.assertIs(type(create_presence()), type({}))

    def test_process_ans(self):
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    def test_process_not_ans(self):
        self.assertNotEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '200 : OK')

    def test_create_person_empty(self):
        self.assertIsNotNone(create_presence(''))

if __name__ == '__main__':
    unittest.main()
