import unittest
from parameterized import parameterized
from iqrfpy.enums.commands import RAMResponseCommands
from iqrfpy.enums.message_types import RAMMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.peripherals.ram.responses import WriteResponse
from iqrfpy.response_factory import ResponseFactory
from tests.helpers.json import generate_json_response

data_ok: dict = {
    'mtype': RAMMessages.WRITE.value,
    'msgid': 'writeTest',
    'nadr': 1,
    'hwpid': 0,
    'rcode': 0,
    'dpa_value': 64,
    'dpa': b'\x01\x00\x05\x81\x00\x00\x00\x40'
}

data_ok_1: dict = {
    'mtype': RAMMessages.WRITE.value,
    'msgid': 'writeTest',
    'nadr': 2,
    'hwpid': 1026,
    'rcode': 0,
    'dpa_value': 35,
    'dpa': b'\x02\x00\x05\x81\x02\x04\x00\x23'
}

data_error: dict = {
    'mtype': RAMMessages.WRITE.value,
    'msgid': 'writeTest',
    'nadr': 0,
    'hwpid': 1026,
    'rcode': 1,
    'dpa_value': 35,
    'dpa': b'\x00\x00\x05\x81\x02\x04\x01\x23'
}


class WriteResponseTestCase(unittest.TestCase):

    @parameterized.expand([
        ['from_dpa', data_ok, ResponseFactory.get_response_from_dpa(data_ok['dpa']), False],
        ['from_dpa', data_ok_1, WriteResponse.from_dpa(data_ok_1['dpa']), False],
        ['from_json', data_ok, ResponseFactory.get_response_from_json(generate_json_response(data_ok)), True],
        ['from_json', data_ok_1, WriteResponse.from_json(generate_json_response(data_ok_1)), True],
        ['from_dpa_error', data_error, WriteResponse.from_dpa(data_error['dpa']), False],
        ['from_json_error', data_error, WriteResponse.from_json(generate_json_response(data_error)), True]
    ])
    def test_factory_methods_ok(self, _, response_data, response, json):
        with self.subTest():
            self.assertEqual(response.nadr, response_data['nadr'])
        with self.subTest():
            self.assertEqual(response.pnum, EmbedPeripherals.RAM)
        with self.subTest():
            self.assertEqual(response.pcmd, RAMResponseCommands.WRITE)
        with self.subTest():
            self.assertEqual(response.hwpid, response_data['hwpid'])
        with self.subTest():
            self.assertEqual(response.rcode, response_data['rcode'])
        if json:
            with self.subTest():
                self.assertEqual(response.mtype, RAMMessages.WRITE)
            with self.subTest():
                self.assertEqual(response.msgid, response_data['msgid'])

    def test_from_dpa_invalid(self):
        with self.assertRaises(ValueError):
            ResponseFactory.get_response_from_dpa(b'\x00\x00\x05\x81\x00\x00\x00\x22\x32')
