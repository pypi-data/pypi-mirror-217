from __future__ import annotations
from typing import Optional, Union
from iqrfpy.enums.commands import SensorRequestCommands
from iqrfpy.enums.message_types import SensorMessages
from iqrfpy.enums.peripherals import Standards
import iqrfpy.utils.dpa as dpa_constants
from iqrfpy.irequest import IRequest

__all__ = ['EnumerateRequest']


class EnumerateRequest(IRequest):

    def __init__(self, nadr: int, hwpid: int = dpa_constants.HWPID_MAX, dpa_rsp_time: Optional[float] = None,
                 dev_process_time: Optional[float] = None, msgid: Optional[str] = None):
        super().__init__(
            nadr=nadr,
            pnum=Standards.SENSOR,
            pcmd=SensorRequestCommands.ENUMERATE,
            m_type=SensorMessages.ENUMERATE,
            hwpid=hwpid,
            dpa_rsp_time=dpa_rsp_time,
            dev_process_time=dev_process_time,
            msgid=msgid
        )

    def to_dpa(self, mutable: bool = False) -> Union[bytes, bytearray]:
        return super().to_dpa(mutable=mutable)

    def to_json(self) -> dict:
        return super().to_json()
