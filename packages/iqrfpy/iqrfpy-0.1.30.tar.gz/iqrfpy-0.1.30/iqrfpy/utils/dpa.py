"""
DPA utility module.

This module contains DPA constants and enum classes.
"""

from .enums import IntEnumMember

__all__ = (
    'RequestPacketMembers',
    'ResponsePacketMembers',
    'COORDINATOR_NADR',
    'NADR_MIN',
    'NADR_MAX',
    'NODE_NADR_MIN',
    'NODE_NADR_MAX',
    'IQUIP_NADR',
    'PNUM_MAX',
    'REQUEST_PCMD_MIN',
    'REQUEST_PCMD_MAX',
    'RESPONSE_PCMD_MIN',
    'RESPONSE_PCMD_MAX',
    'HWPID_MIN',
    'HWPID_MAX',
    'CONFIRMATION_PACKET_LEN',
    'RESPONSE_GENERAL_LEN',
    'THERMOMETER_SENSOR_ERROR',
    'THERMOMETER_RESOLUTION',
    'MID_MIN',
    'MID_MAX',
    'LOCAL_DEVICE_ADDR',
    'IQMESH_TEMP_ADDR',
    'BROADCAST_ADDR',
    'BYTE_MIN',
    'BYTE_MAX',
    'WORD_MIN',
    'WORD_MAX',
    'REQUEST_PDATA_MAX_LEN',
    'RESPONSE_PDATA_MAX_LEN',
    'SENSOR_INDEX_MIN',
    'SENSOR_INDEX_MAX',
    'BaudRates',
    'ResponseCodes',
    'PeripheralTypes',
    'ExtendedPeripheralCharacteristics',
    'UserFrcCommands',
    'FrcResponseTimes'
)


class RequestPacketMembers(IntEnumMember):
    """Request packet member indices."""

    NADR = 0
    PNUM = 2
    PCMD = 3
    HWPID_LO = 4
    HWPID_HI = 5


class ResponsePacketMembers(IntEnumMember):
    """Response packet member indices."""

    NADR = 0
    PNUM = 2
    PCMD = 3
    HWPID_LO = 4
    HWPID_HI = 5
    RCODE = 6
    DPA_VALUE = 7


# general constants
COORDINATOR_NADR = NADR_MIN = 0
NODE_NADR_MIN = 0x01
NADR_MAX = NODE_NADR_MAX = 0xEF
IQUIP_NADR = 0xF0
PNUM_MAX = 0x7F
REQUEST_PCMD_MIN = 0
REQUEST_PCMD_MAX = 0x7F
RESPONSE_PCMD_MIN = 0x80
RESPONSE_PCMD_MAX = 0xFF
HWPID_MIN = 0
HWPID_MAX = 0xFFFF

# confirmation constants
CONFIRMATION_PACKET_LEN = 11

# response constants
RESPONSE_GENERAL_LEN = 8

# thermometer constants
THERMOMETER_SENSOR_ERROR = 0x80
THERMOMETER_RESOLUTION = 0.0625

# mid constants
MID_MIN = 0
MID_MAX = 0xFFFFFFFF

# other constants
IBK_LEN = 16
LOCAL_DEVICE_ADDR = 0xFC
IQMESH_TEMP_ADDR = 0xFE
BROADCAST_ADDR = 0xFF
BYTE_MIN = 0
BYTE_MAX = 255
WORD_MIN = 0
WORD_MAX = 65535

REQUEST_PDATA_MAX_LEN = 58
RESPONSE_PDATA_MAX_LEN = 56

SENSOR_INDEX_MIN = 0
SENSOR_INDEX_MAX = 31


class BaudRates(IntEnumMember):
    """UART baud rate constants."""

    B1200 = 0
    B2400 = 1
    B4800 = 2
    B9600 = 3
    B19200 = 4
    B38400 = 5
    B57600 = 6
    B115200 = 7
    B230400 = 8


# rcode constants
class ResponseCodes(IntEnumMember):
    """DPA response codes."""

    OK = 0
    ERROR_FAIL = 1
    ERROR_PCMD = 2
    ERROR_PNUM = 3
    ERROR_ADDR = 4
    ERROR_DATA_LEN = 5
    ERROR_DATA = 6
    ERROR_HWPID = 7
    ERROR_NADR = 8
    ERROR_IFACE_CUSTOM_HANDLER = 9
    ERROR_MISSING_CUSTOM_DPA_HANDLER = 10
    ERROR_USER_FROM = 0x20
    ERROR_USER_TO = 0x3F
    RESERVED_FLAG = 0x40
    ASYNC_RESPONSE = 0x80
    CONFIRMATION = 0xFF

    def __str__(self):
        """Convert self to representation of error code."""
        return self.to_string(self.value)

    @classmethod
    def to_string(cls, value: int):
        """
        Convert value to string representation of error code.

        Args:
            value (int): Value to convert

        Returns:
            str: String representation of error code
        """
        if not (BYTE_MIN <= value <= BYTE_MAX):
            return 'Invalid DPA response code'
        if cls.ERROR_USER_FROM <= value <= cls.ERROR_USER_TO:
            return 'User error code'
        flags = []
        if value & 0x40:
            flags.append('reserved')
            value -= 0x40
        if value & 0x80:
            flags.append('async')
            value -= 0x80
        if value not in cls._value2member_map_:
            return 'Unknown DPA response code'
        val = cls(value)
        str_val = None
        match val:
            case cls.OK:
                str_val = 'No error'
            case cls.ERROR_FAIL:
                str_val = 'General fail'
            case cls.ERROR_PCMD:
                str_val = 'Incorrect PCMD'
            case cls.ERROR_PNUM:
                str_val = 'Incorrect PNUM or PCMD'
            case cls.ERROR_ADDR:
                str_val = 'Incorrect Address'
            case cls.ERROR_DATA_LEN:
                str_val = 'Incorrect Data length'
            case cls.ERROR_DATA:
                str_val = 'Incorrect Data'
            case cls.ERROR_HWPID:
                str_val = 'Incorrect HW Profile ID used'
            case cls.ERROR_NADR:
                str_val = 'Incorrect NADR'
            case cls.ERROR_IFACE_CUSTOM_HANDLER:
                str_val = 'Data from interface consumed by Custom DPA Handler'
            case cls.ERROR_MISSING_CUSTOM_DPA_HANDLER:
                str_val = 'Custom DPA Handler is missing'
            case cls.CONFIRMATION:
                str_val = 'DPA confirmation'
        flag_str = '' if len(flags) == 0 else ''.join(f' [{flag}]' for flag in flags)
        return f'{str_val}{flag_str}'


class PeripheralTypes(IntEnumMember):
    """Peripheral type constants."""

    PERIPHERAL_TYPE_DUMMY = 0
    PERIPHERAL_TYPE_COORDINATOR = 1
    PERIPHERAL_TYPE_NODE = 2
    PERIPHERAL_TYPE_OS = 3
    PERIPHERAL_TYPE_EEPROM = 4
    PERIPHERAL_TYPE_BLOCK_EEPROM = 5
    PERIPHERAL_TYPE_RAM = 6
    PERIPHERAL_TYPE_LED = 7
    PERIPHERAL_TYPE_SPI = 8
    PERIPHERAL_TYPE_IO = 9
    PERIPHERAL_TYPE_UART = 10
    PERIPHERAL_TYPE_THERMOMETER = 11
    PERIPHERAL_TYPE_FRC = 14


class ExtendedPeripheralCharacteristics(IntEnumMember):
    """Extended peripheral characteristics constants."""

    PERIPHERAL_TYPE_EXTENDED_DEFAULT = 0
    PERIPHERAL_TYPE_EXTENDED_READ = 1
    PERIPHERAL_TYPE_EXTENDED_WRITE = 2
    PERIPHERAL_TYPE_EXTENDED_READ_WRITE = 3


class UserFrcCommands(IntEnumMember):
    """User FRC command intervals."""

    USER_BIT_FROM = 0x40
    USER_BIT_TO = 0x7F
    USER_BYTE_FROM = 0xC0
    USER_BYTE_TO = 0xDF
    USER_2BYTE_FROM = 0xF0
    USER_2BYTE_TO = 0xFF
    USER_4BYTE_FROM = 0xFC
    USER_4BYTE_TO = 0xFF


class FrcResponseTimes(IntEnumMember):
    """FRC response time constants."""

    MS40 = 0
    MS360 = 16
    MS680 = 32
    MS1320 = 48
    MS2600 = 64
    MS5160 = 80
    MS10280 = 96
    MS20520 = 112
