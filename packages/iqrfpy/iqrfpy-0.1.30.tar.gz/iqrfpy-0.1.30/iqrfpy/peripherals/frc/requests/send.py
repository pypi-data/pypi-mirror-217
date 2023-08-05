from __future__ import annotations
from typing import List, Optional, Union
from iqrfpy.enums.commands import FrcRequestCommands
from iqrfpy.enums.message_types import FrcMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.exceptions import RequestParameterInvalidValueError
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['SendRequest']


class SendRequest(IRequest):

    __slots__ = '_frc_command', '_user_data'

    def __init__(self, nadr: int, frc_command: int, user_data: List[int], hwpid: int = dpa_constants.HWPID_MAX,
                 dpa_rsp_time: Optional[float] = None, dev_process_time: Optional[float] = None,
                 msgid: Optional[str] = None):
        self._validate(frc_command, user_data)
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.FRC,
            pcmd=FrcRequestCommands.SEND,
            m_type=FrcMessages.SEND,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )
        self._frc_command = frc_command
        self._user_data = user_data

    def _validate(self, frc_command: int, user_data: List[int]):
        self._validate_frc_command(frc_command)
        self._validate_user_data(user_data)

    @staticmethod
    def _validate_frc_command(frc_command: int):
        if not (dpa_constants.BYTE_MIN <= frc_command <= dpa_constants.BYTE_MAX):
            raise RequestParameterInvalidValueError('FRC command value should be between 0 and 255.')

    @property
    def frc_command(self):
        return self._frc_command

    @frc_command.setter
    def frc_command(self, value: int):
        self._validate_frc_command(value)
        self._frc_command = value

    @staticmethod
    def _validate_user_data(user_data: List[int]):
        if len(user_data) > 57:
            raise RequestParameterInvalidValueError('User data should be at most 57 bytes long.')
        if not Common.values_in_byte_range(user_data):
            raise RequestParameterInvalidValueError('User data values should be between 0 and 255.')

    @property
    def user_data(self) -> List[int]:
        return self._user_data

    @user_data.setter
    def user_data(self, value: List[int]):
        self._validate_user_data(value)
        self._user_data = value

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        self._pdata = [self._frc_command] + self._user_data
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        self._params = {'frcCommand': self._frc_command, 'userData': self._user_data}
        return super().to_json()
