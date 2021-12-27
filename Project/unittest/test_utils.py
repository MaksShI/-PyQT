import unittest

import socket
import sys
import json
import os

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, \
    DEFAULT_IP_ADDRESS, ENCODING
from common.utils import get_message, send_message


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.receved_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.receved_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestSalary(unittest.TestCase):
    test_out = {
        ACTION: PRESENCE,
        TIME: 21,
        USER: {
            ACCOUNT_NAME: 'account_name'
        }
    }
    test_response = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    test_good_response = {RESPONSE: 200}

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_send_None_message(self):
        self.assertIsNone(
            send_message(TestSocket({RESPONSE: 400, ERROR: 'Bad Request'}), {RESPONSE: 400, ERROR: 'Bad Request'}))

    def test_send_message(self):
        self.assertEqual(
            send_message(TestSocket(test_dict={ACTION: PRESENCE, TIME: 21, USER: {ACCOUNT_NAME: 'account_name'}}),
                         {ACTION: PRESENCE, TIME: 21, USER: {ACCOUNT_NAME: 'account_name'}}), None)

#    def test_get_message(self):
#        self.assertEqual(get_message(TestSocket(test_dict={ACTION: PRESENCE, TIME: 21, USER: {ACCOUNT_NAME: 'account_name'}})))
