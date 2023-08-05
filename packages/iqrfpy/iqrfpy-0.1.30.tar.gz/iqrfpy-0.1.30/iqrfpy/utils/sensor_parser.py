"""
Sensor parser module.

Provides methods for parsing of sensor data collected by DPA and JSON API requests.
"""

import math
from dataclasses import dataclass
from typing import List, Union
from iqrfpy.exceptions import UnknownSensorTypeError
from iqrfpy.utils.sensor_constants import SensorDataSize, SensorTypes, SensorFrcCommands, SensorFrcErrors
from iqrfpy.utils.common import Common
from iqrfpy.utils.quantity_data import get_sensor_class


@dataclass
class SensorData:
    """Class representing Sensor (quantity) information and value."""

    __slots__ = 'sensor_type', 'index', 'name', 'short_name', 'unit', 'decimal_places', 'frc_commands', 'value'

    sensor_type: SensorTypes
    index: int
    name: str
    short_name: str
    unit: str
    decimal_places: int
    frc_commands: List[int]
    value: Union[int, float, List[int], SensorFrcErrors, None]

    def __init__(self, sensor_type: SensorTypes, index: int, name: str,
                 short_name: str, unit: str, decimal_places: int, frc_commands: List[int],
                 value: Union[int, float, List[int], SensorFrcErrors, None] = None):
        """Class representing Sensor (quantity) information and value.

        Args:
            sensor_type (SensorTypes): Sensor type (represents a quantity)
            index (int): Index of sensor
            name (str): Quantity name
            short_name (str): Short quantity name
            unit (str): Quantity unit
            decimal_places (int): Precision
            frc_commands (List[int]): Implemented FRC commands
            value (Union[int, float, List[int], SensorFrcErrors, None]): Measured value
        """
        self.sensor_type = sensor_type
        self.index = index
        self.name = name
        self.short_name = short_name
        self.unit = unit
        self.decimal_places = decimal_places
        self.frc_commands = frc_commands
        self.value = value


class SensorParser:
    """Class for parsing data from Sensor standard response data."""

    @classmethod
    def enumerate_from_dpa(cls, dpa: List[int]) -> List[SensorData]:
        """
        Process data from Enumerate DPA response into a list of SensorData objects.

        Note that Enumerate request only provides sensor types (quantities), as such, the SensorData objects
        produced by this method will not carry a value.

        Args:
            dpa (List[int]): List of pdata bytes from DPA response

        Returns:
            List[SensorData]: List of SensorData objects containing parsed data

        Raises:
            UnknownSensorTypeError: Raised if sensor type is passed as integer and the value is not recognized
        """
        sensor_data = []
        for i in range(len(dpa)):
            sensor_type_value = dpa[i]
            if not SensorTypes.has_value(sensor_type_value):
                raise UnknownSensorTypeError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            sensor_class = get_sensor_class(sensor_type)
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=len(sensor_data),
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands
                )
            )
        return sensor_data

    @classmethod
    def enumerate_from_json(cls, json_data: List[dict]) -> List[SensorData]:
        """
        Process data from Enumerate API response into a list of SensorData objects.

        Note that Enumerate request only provides sensor types (quantities), as such, the SensorData objects
        produced by this method will not carry a value.

        Args:
            json_data (List[dict]): List of json objects from JSON API response

        Returns:
            List[SensorData]: List of SensorData objects containing parsed data

        Raises:
            UnknownSensorTypeError: Raised if sensor type is passed as integer and the value is not recognized
        """
        sensor_data = []
        for i in range(len(json_data)):
            data = json_data[i]
            sensor_type_value = data['type']
            if not SensorTypes.has_value(sensor_type_value):
                raise UnknownSensorTypeError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            sensor_class = get_sensor_class(sensor_type)
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=len(sensor_data),
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands
                )
            )
        return sensor_data

    @classmethod
    def read_sensors_dpa(cls, sensor_types: List[int], dpa: List[int]) -> List[SensorData]:
        """
        Process data from ReadSensor DPA response into a list of SensorData objects.

        Because the ReadSensors DPA response does not carry information about sensor types,
        it is necessary to provide sensor types for response data.

        Args:
            sensor_types (List[int]): List of sensor types
            dpa (List[int]): List of pdata bytes from DPA response

        Returns:
            List[SensorData]: List of SensorData objects containing parsed data

        Raises:
            UnknownSensorTypeError: Raised if sensor type is passed as integer and the value is not recognized
            ValueError: Raised if passed data is shorter than required to process all sensors
        """
        sensor_data = []
        data_index = 0
        sensor_index = 0
        while data_index < len(dpa):
            if sensor_index >= len(sensor_types):
                raise ValueError('Too little sensor types provided for the amount of sensor data.')
            sensor_type_value = sensor_types[sensor_index]
            if not SensorTypes.has_value(sensor_type_value):
                raise UnknownSensorTypeError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            if sensor_type == SensorTypes.DATA_BLOCK:
                data_len = dpa[data_index]
                if data_index + data_len >= len(dpa):
                    raise ValueError('Data length longer than actual data.')
            else:
                data_len = _data_len_from_type(sensor_type)
                if data_index + data_len > len(dpa):
                    raise ValueError('Data length longer than actual data.')
            sensor_data.extend([sensor_type_value] + dpa[data_index:data_index + data_len])
            data_index += data_len
            sensor_index += 1
        return cls.read_sensors_with_types_from_dpa(sensor_data)

    @classmethod
    def read_sensors_with_types_from_dpa(cls, dpa: List[int]) -> List[SensorData]:
        """
        Process data from ReadSensorWithTypes DPA response into a list of SensorData objects.

        Args:
            dpa (List[int]): List of pdata bytes from DPA response

        Returns:
            List[SensorData]: List of SensorData objects containing parsed data

        Raises:
            UnknownSensorTypeError: Raised if sensor type is passed as integer and the value is not recognized
            ValueError: Raised if passed data is shorter than required to process all sensors
        """
        sensor_data = []
        index = 0
        while index < len(dpa):
            sensor_type_value = dpa[index]
            if not SensorTypes.has_value(sensor_type_value):
                raise UnknownSensorTypeError(f'Unsupported sensor type: {sensor_type_value}.')
            sensor_type = SensorTypes(sensor_type_value)
            if sensor_type == SensorTypes.DATA_BLOCK:
                data_length = dpa[index + 1]
                if index + 1 + data_length >= len(dpa):
                    raise ValueError('Data length is less than expected to process all sensors.')
                data = dpa[index + 2:index + 2 + data_length]
            else:
                data_length = _data_len_from_type(sensor_type)
                if index + data_length >= len(dpa):
                    raise ValueError('Data length is less than expected to process all sensors.')
                data = cls.convert(sensor_type, dpa[index + 1:index + 1 + data_length])
            sensor_class = get_sensor_class(sensor_type)
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=len(sensor_data),
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands,
                    value=data
                )
            )
            index += (data_length + 1)
        return sensor_data

    @classmethod
    def read_sensors_with_types_from_json(cls, json_data: List[dict]) -> List[SensorData]:
        """
        Process data from ReadSensorWithTypes API response into a list of SensorData objects.

        Args:
            json_data (List[dict]): List of json objects from JSON API response

        Returns:
            List[SensorData]: List of SensorData objects containing parsed data

        Raises:
            UnknownSensorTypeError: Raised if sensor type is passed as integer and the value is not recognized
        """
        sensor_data = []
        for i in range(len(json_data)):
            data = json_data[i]
            sensor_type_value = data['type']
            if not SensorTypes.has_value(sensor_type_value):
                raise UnknownSensorTypeError('Unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type_value)
            sensor_class = get_sensor_class(sensor_type)
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=len(sensor_data),
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands,
                    value=data['value']
                )
            )
        return sensor_data

    @classmethod
    def frc_dpa(cls, sensor_type: Union[SensorTypes, int], sensor_index: int, frc_command: Union[SensorFrcCommands, int],
                data: List[int], extra_result: List[int] = [], count: Union[int, None] = None) -> List[SensorData]:
        """
        Process data from DPA FRC response into a list of SensorData.

        SensorData object contains information about the measured quantity and converted value.
        The data argument expects only FRC data bytes, without the status byte.
        The extra_result argument can be omitted if the processed data fit into just the Send or SendSelective response.

        If count is specified, only that number of node data is processed.
        For example, if total length of passed data is 64 bytes (which includes extra result data) and data length
        per node is 2 bytes, and only 3 nodes are to be processed, then only first 6 bytes of the passed data will be
        processed and returned as SensorData objects.

        If count is not specified and combined length of passed FRC and extra result data is not equal to the number
        of bytes required to process as many nodes as a single Send (SendSelective) and ExtraResult request can carry,
        a ValueError is raised.

        Args:
            sensor_type (Union[SensorTypes, int]): Sensor type (represents a quantity)
            sensor_index (int): Index of sensor
            frc_command (int): FRC command used to collect data
            data (List[int]): Data collected from Send or SendSelective message
            extra_result (List[int]): Data collected from ExtraResult message
            count (Union[int, None]): Specifies number of nodes to process

        Returns:
            List[SensorData]: List of SensorData objects containing parsed data

        Raises:
            UnknownSensorTypeError: Raised if sensor type is passed as integer and the value is not recognized
            ValueError: Raised if combined length of frc data and extra result does not match the required data
                        length to process nodes regardless of count argument value
        """
        if isinstance(sensor_type, int):
            if not SensorTypes.has_value(sensor_type):
                raise UnknownSensorTypeError('Unknown or unsupported sensor type.')
            sensor_type = SensorTypes(sensor_type)
        sensor_class = get_sensor_class(sensor_type)
        dpa = data
        if frc_command == SensorFrcCommands.FRC_1BYTE:
            dpa = data[1:]
        elif frc_command == SensorFrcCommands.FRC_2BYTES:
            dpa = data[2:]
        elif frc_command == SensorFrcCommands.FRC_4BYTES:
            dpa = data[4:]
        if extra_result is not None:
            dpa.extend(extra_result)
        data_len = _data_len_from_frc_command(frc_command=frc_command)
        if count is None:
            if frc_command != SensorFrcCommands.FRC_2BITS and len(dpa) % data_len != 0:
                raise ValueError('Invalid length of combined frc data and extra result data.')
        else:
            if frc_command != SensorFrcCommands.FRC_2BITS:
                if len(dpa) < count * data_len:
                    raise ValueError(f'Combined length of frc data and extra result is less than length of data'
                                     f'required to process {count} devices.')
                dpa = dpa[:count * data_len]
        if data_len == 0.25:
            itr = count + 1 if count is not None else 240
            frc_values = []
            for i in range(1, itr):
                mask = 1 << (i % 8)
                idx = math.floor(i / 8)
                if idx + 32 >= len(dpa):
                    raise ValueError('Combined length of frc data and extra result is too short.')
                val = 0
                if (dpa[idx] & mask) != 0:
                    val = 1
                if (dpa[idx + 32] & mask) != 0:
                    val |= 2
                frc_values.append(val)
        elif data_len == 1:
            frc_values = dpa
        elif data_len == 2:
            frc_values = [(dpa[i + 1] << 8) + dpa[i] for i in range(0, len(dpa), 2)]
        else:
            frc_values = [(dpa[i + 3] << 24) + (dpa[i + 2] << 16) + (dpa[i + 1] << 8) + dpa[i] for i in range(0, len(dpa), 4)]
        sensor_data = []
        for frc_value in frc_values:
            sensor_data.append(
                SensorData(
                    sensor_type=sensor_type,
                    index=sensor_index,
                    name=sensor_class.name,
                    short_name=sensor_class.short_name,
                    unit=sensor_class.unit,
                    decimal_places=sensor_class.decimal_places,
                    frc_commands=sensor_class.frc_commands,
                    value=cls.frc_convert(sensor_type, frc_command, frc_value) if sensor_type != SensorTypes.DATA_BLOCK else frc_values
                )
            )
        return sensor_data

    @staticmethod
    def convert(sensor_type: Union[SensorTypes, int], values: List[int]) -> Union[int, float, List[int], None]:
        """
        Convert sensor data to a value within the range of quantity specified by sensor type.

        Args:
            sensor_type (Union[SensorTypes, int]): Sensor type (represents a quantity)
            values: (List[int]): Collected data to convert

        Returns:
            Union[int, float, List[int], None]: Converted value
        """
        match sensor_type:
            case SensorTypes.TEMPERATURE | SensorTypes.LOW_VOLTAGE:
                sensor_value = values[0] + (values[1] << 8)
                return Common.word_complement(sensor_value) / 16.0 if sensor_value != 0x8000 else None
            case SensorTypes.ATMOSPHERIC_PRESSURE:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value / 16.0 if sensor_value != 0xFFFF else None
            case SensorTypes.CARBON_DIOXIDE | SensorTypes.VOLATILE_ORGANIC_COMPOUND | SensorTypes.COLOR_TEMPERATURE:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value if sensor_value != 0x8000 else None
            case SensorTypes.TIME_SPAN | SensorTypes.ILLUMINANCE | SensorTypes.TOTAL_VOLATILE_ORGANIC_COMPOUND | \
                    SensorTypes.NITROGEN_OXIDES:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value if sensor_value != 0xFFFF else None
            case SensorTypes.EXTRA_LOW_VOLTAGE | SensorTypes.CURRENT:
                sensor_value = values[0] + (values[1] << 8)
                return Common.word_complement(sensor_value) / 1000.0 if sensor_value != 0x8000 else None
            case SensorTypes.MAINS_FREQUENCY | SensorTypes.NITROGEN_DIOXIDE | SensorTypes.SULFUR_DIOXIDE | \
                    SensorTypes.METHANE | SensorTypes.SHORT_LENGTH:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value / 1000.0 if sensor_value != 0xFFFF else None
            case SensorTypes.EARTHS_MAGNETIC_FIELD:
                sensor_value = values[0] + (values[1] << 8)
                return Common.word_complement(sensor_value) / 10000000.0 if sensor_value != 0x8000 else None
            case SensorTypes.POWER:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value / 4.0 if sensor_value != 0xFFFF else None
            case SensorTypes.CARBON_MONOXIDE:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value / 100.0 if sensor_value != 0xFFFF else None
            case SensorTypes.OZONE:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value / 10000.0 if sensor_value != 0xFFFF else None
            case SensorTypes.PARTICULATES_PM2_5 | SensorTypes.PARTICULATES_PM1 | SensorTypes.PARTICULATES_PM4 | \
                    SensorTypes.PARTICULATES_PM10:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value / 4.0 if sensor_value != 0x8000 else None
            case SensorTypes.SOUND_PRESSURE_LEVEL:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value / 16.0 if sensor_value != 0x8000 else None
            case SensorTypes.ALTITUDE:
                sensor_value = values[0] + (values[1] << 8)
                return (sensor_value / 4.0 - 1024) if sensor_value != 0xFFFF else None
            case SensorTypes.ACCELERATION:
                sensor_value = values[0] + (values[1] << 8)
                return Common.word_complement(sensor_value) / 256.0 if sensor_value != 0x8000 else None
            case SensorTypes.AMMONIA:
                sensor_value = values[0] + (values[1] << 8)
                return sensor_value / 10.0 if sensor_value != 0xFFFF else None
            case SensorTypes.RELATIVE_HUMIDITY:
                return values[0] / 2.0 if values[0] != 0xEE else None
            case SensorTypes.BINARY_DATA7:
                aux = values[0] & 0x80
                return values[0] if aux == 0 else None
            case SensorTypes.POWER_FACTOR:
                return values[0] / 200.0 if values[0] != 0xEE else None
            case SensorTypes.UV_INDEX:
                return values[0] / 8.0 if values[0] != 0xFF else None
            case SensorTypes.PH:
                return values[0] / 16.0 if values[0] != 0xFF else None
            case SensorTypes.RSSI:
                return (values[0] - 254) / 2.0 if values[0] != 0xFF else None
            case SensorTypes.BINARY_DATA30:
                sensor_value = values[0] + (values[1] << 8) + (values[2] << 16) + (values[3] << 24)
                return sensor_value if (values[3] & 0x80) == 0 else None
            case SensorTypes.CONSUMPTION | SensorTypes.DATETIME:
                sensor_value = values[0] + (values[1] << 8) + (values[2] << 16) + (values[3] << 24)
                return sensor_value if sensor_value != 0xFFFFFFFF else None
            case SensorTypes.TIME_SPAN_LONG:
                sensor_value = values[0] + (values[1] << 8) + (values[2] << 16) + (values[3] << 24)
                return sensor_value / 16.0 if sensor_value != 0xFFFFFFFF else None
            case SensorTypes.LATITUDE | SensorTypes.LONGITUDE:
                if values[0] == 0xFF or (values[2] & 0x40) == 0:
                    return None
                sensor_value = values[3] + ((values[2] & 0x3F) + (values[0] + (values[1] << 8)) / 10000) / 60
                if (values[2] & 0x80) != 0:
                    sensor_value = -sensor_value
                return sensor_value
            case SensorTypes.DATETIME:
                length = values[0]
                return values[1:1 + length]
            case _:
                return None

    @staticmethod
    def frc_convert(sensor_type: Union[SensorTypes, int], frc_command: int, frc_value: int) -> Union[int, float, None]:
        """
        Convert data collected from FRC to a value within the range of quantity specified by sensor type.

        Args:
            sensor_type (Union[SensorTypes, int]): Sensor type (represents a quantity)
            frc_command (int): FRC command used when collecting data
            frc_value (int): Raw data to convert

        Returns:
            Union[int, float, None]: Converted value
        """
        value = None
        if frc_command == SensorFrcCommands.FRC_2BITS:
            if 0 <= frc_value <= 1:
                return SensorFrcErrors(frc_value)
        else:
            if 0 <= frc_value <= 3:
                return SensorFrcErrors(frc_value)
        match sensor_type:
            case SensorTypes.TEMPERATURE:
                if frc_command == SensorFrcCommands.FRC_1BYTE:
                    value = frc_value / 2.0 - 22
                elif frc_command == SensorFrcCommands.FRC_2BYTES:
                    value = Common.word_complement(frc_value ^ 0x8000) / 16.0
            case SensorTypes.LOW_VOLTAGE:
                value = Common.word_complement(frc_value ^ 0x8000) / 16.0
            case SensorTypes.ATMOSPHERIC_PRESSURE | SensorTypes.SOUND_PRESSURE_LEVEL | SensorTypes.TIME_SPAN_LONG:
                value = (frc_value - 4) / 16.0
            case SensorTypes.CARBON_DIOXIDE | SensorTypes.VOLATILE_ORGANIC_COMPOUND:
                if frc_command == SensorFrcCommands.FRC_1BYTE:
                    value = (frc_value - 4) * 16
                elif frc_command == SensorFrcCommands.FRC_2BYTES:
                    value = frc_value - 4
            case SensorTypes.COLOR_TEMPERATURE | SensorTypes.TIME_SPAN | SensorTypes.ILLUMINANCE | \
                    SensorTypes.CONSUMPTION | SensorTypes.DATETIME | SensorTypes.TOTAL_VOLATILE_ORGANIC_COMPOUND | \
                    SensorTypes.NITROGEN_OXIDES:
                value = frc_value - 4
            case SensorTypes.EXTRA_LOW_VOLTAGE | SensorTypes.CURRENT:
                value = Common.word_complement(frc_value ^ 0x8000) / 1000.0
            case SensorTypes.EARTHS_MAGNETIC_FIELD:
                value = Common.word_complement(frc_value ^ 0x8000) / 10000000.0
            case SensorTypes.POWER | SensorTypes.PARTICULATES_PM1 | SensorTypes.PARTICULATES_PM2_5 | \
                    SensorTypes.PARTICULATES_PM4 | SensorTypes.PARTICULATES_PM10:
                value = (frc_value - 4) / 4.0
            case SensorTypes.CARBON_MONOXIDE:
                value = (frc_value - 4) / 100.0
            case SensorTypes.OZONE:
                value = (frc_value - 4) / 10000.0
            case SensorTypes.ALTITUDE:
                value = (Common.word_complement(frc_value ^ 0x8000) / 4.0) - 1024
            case SensorTypes.ACCELERATION:
                value = (Common.word_complement(frc_value) - 4) / 256.0
            case SensorTypes.AMMONIA:
                value = (frc_value - 4) / 10.0
            case SensorTypes.RELATIVE_HUMIDITY:
                value = (frc_value - 4) / 2.0
            case SensorTypes.BINARY_DATA7:
                if frc_command == SensorFrcCommands.FRC_2BITS:
                    value = frc_value & 0x01
                elif frc_command == SensorFrcCommands.FRC_1BYTE:
                    value = frc_value - 4
            case SensorTypes.POWER_FACTOR:
                value = (frc_value - 4) / 200.0
            case SensorTypes.UV_INDEX:
                value = (frc_value - 4) / 8.0
            case SensorTypes.PH:
                value = (frc_value - 4) / 16.0
            case SensorTypes.RSSI:
                value = (frc_value - 258) / 2.0
            case SensorTypes.BINARY_DATA30:
                if frc_command == SensorFrcCommands.FRC_2BYTES or frc_command == SensorFrcCommands.FRC_4BYTES:
                    value = frc_value - 4
            case SensorTypes.LATITUDE | SensorTypes.LONGITUDE:
                value = frc_value
        return value


def _data_len_from_type(sensor_type: Union[SensorTypes, int]):
    """
    Return expected data length per node for sensor type.

    Args:
        sensor_type (Union[SensorTypes, int]): Sensor type (represents a quantity)

    Returns:
        int: Expected data length per node

    Raises:
        UnknownSensorTypeError: Raised if sensor_type value is an unknown or unsupported sensor type
    """
    if SensorDataSize.DATA_1BYTE_MIN <= sensor_type <= SensorDataSize.DATA_1BYTE_MAX:
        return 1
    elif SensorDataSize.DATA_2BYTES_MIN <= sensor_type <= SensorDataSize.DATA_2BYTES_MAX:
        return 2
    elif SensorDataSize.DATA_4BYTES_MIN <= sensor_type <= SensorDataSize.DATA_4BYTES_MAX:
        return 4
    else:
        raise UnknownSensorTypeError('Unsupported sensor type.')


def _data_len_from_frc_command(frc_command: Union[SensorFrcCommands, int]):
    """
    Return expected data length per node collected by FRC command.

    Args:
        frc_command (Union[SensorFrcCommands, int]): Sensor FRC command

    Returns:
        int: Expected data length per node

    Raises:
        ValueError: Raised if frc_command value is unknown or unsupported Sensor FRC command
    """
    if frc_command == SensorFrcCommands.FRC_2BITS:
        return 0.25
    if frc_command == SensorFrcCommands.FRC_1BYTE:
        return 1
    if frc_command == SensorFrcCommands.FRC_2BYTES:
        return 2
    if frc_command == SensorFrcCommands.FRC_4BYTES:
        return 4
    else:
        raise ValueError('Unsupported frc command')
