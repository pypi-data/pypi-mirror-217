from __future__ import annotations
from typing import List, Optional
from iqrfpy.iresponse import IResponseGetterMixin
from iqrfpy.enums.commands import NodeResponseCommands
from iqrfpy.enums.message_types import NodeMessages
from iqrfpy.enums.peripherals import EmbedPeripherals
from iqrfpy.utils.common import Common
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.utils.dpa import ResponsePacketMembers
from iqrfpy.utils.validators import DpaValidator, JsonValidator

__all__ = ['ValidateBondsResponse']


class ValidateBondsResponse(IResponseGetterMixin):

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, rcode: int = 0, dpa_value: int = 0,
                 msgid: Optional[str] = None, pdata: Optional[List[int]] = None, result: Optional[dict] = None):
        super().__init__(
            nadr=nadr,
            pnum=EmbedPeripherals.NODE,
            pcmd=NodeResponseCommands.VALIDATE_BONDS,
            m_type=NodeMessages.VALIDATE_BONDS,
            hwpid=hwpid,
            rcode=rcode,
            dpa_value=dpa_value,
            msgid=msgid,
            pdata=pdata,
            result=result
        )

    @staticmethod
    def from_dpa(dpa: bytes) -> ValidateBondsResponse:
        DpaValidator.base_response_length(dpa=dpa)
        nadr = dpa[ResponsePacketMembers.NADR]
        hwpid = Common.hwpid_from_dpa(dpa[ResponsePacketMembers.HWPID_HI], dpa[ResponsePacketMembers.HWPID_LO])
        rcode = dpa[ResponsePacketMembers.RCODE]
        dpa_value = dpa[ResponsePacketMembers.DPA_VALUE]
        DpaValidator.response_length(dpa=dpa, expected_len=8)
        return ValidateBondsResponse(nadr=nadr, hwpid=hwpid, rcode=rcode, dpa_value=dpa_value, result=None)

    @staticmethod
    def from_json(json: dict) -> ValidateBondsResponse:
        JsonValidator.response_received(json=json)
        msgid = Common.msgid_from_json(json=json)
        nadr = Common.nadr_from_json(json=json)
        hwpid = Common.hwpid_from_json(json=json)
        dpa_value = Common.dpa_value_from_json(json=json)
        rcode = Common.rcode_from_json(json=json)
        return ValidateBondsResponse(nadr=nadr, msgid=msgid, hwpid=hwpid, dpa_value=dpa_value, rcode=rcode, result=None)
