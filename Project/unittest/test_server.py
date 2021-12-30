import os
import sys
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from server import process_client_message
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT


# {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: account_name}}

class TestSalary(unittest.TestCase):
    def test_process_client_message(self):
        self.assertEqual(process_client_message('200 : OK'), {'response': 400, 'error': 'Bad Request'})

    def test_process_client_message_is(self):
        self.assertIs(type(process_client_message('200 : OK')), type({}))

    def test_process_client_message_empty(self):
        self.assertEqual(process_client_message(''), {'response': 400, 'error': 'Bad Request'})

    def test_process_client_message_action(self):
        self.assertIsNotNone(process_client_message({ACTION: ''}))

    def test_process_client_message_Time(self):
        self.assertEqual(process_client_message({ACTION: '', TIME: 11}), {'response': 400, 'error': 'Bad Request'})

    def test_process_client_message_User(self):
        self.assertEqual(process_client_message({ACTION: PRESENCE, TIME: 11, USER: {ACCOUNT_NAME: 'Guest'}}),
                         {RESPONSE: 200})


if __name__ == '__main__':
    unittest.main()
