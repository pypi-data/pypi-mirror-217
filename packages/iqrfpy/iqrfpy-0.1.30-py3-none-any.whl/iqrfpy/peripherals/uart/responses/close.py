from __future__ import annotations
from typing import Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import UartResponseCommands
from iqrfpy.enums.message_types import UartMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponsePacketMembers
from iqrfpy.utils.validators import DpaValidator, JsonValidator


class CloseResponse(IResponseGetterMixin):

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.UART,
            pcmd=UartResponseCommands.CLOSE,
            m_type=UartMessages.CLOSE,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            result=result
        )

    @staticmethod
    def from_dpa(dpa: bytes) -> CloseResponse:
        DpaValidator.base_response_length(dpa=dpa)
        DpaValidator.response_length(dpa=dpa, expected_len=8)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        return CloseResponse(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, result=None)

    @staticmethod
    def from_json(json: dict) -> CloseResponse:
        JsonValidator.response_received(json=json)
        msgid = Common.msgid_from_json(json=json)
        nadr = Common.nadr_from_json(json=json)
        hwpid = Common.hwpid_from_json(json=json)
        dpa_value = Common.dpa_value_from_json(json=json)
        rcode = Common.rcode_from_json(json=json)
        return CloseResponse(nadr=nadr, msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, result=None)
