# -*- coding: utf-8 -*-
"""
Defines the STOCKS models
"""
from jsonpickle import handlers
from cli.utils import Technology, SequencingRunType, SequencingReadType, JsonEnumHandler

handlers.registry.register(Technology, JsonEnumHandler)
handlers.registry.register(SequencingReadType, JsonEnumHandler)
handlers.registry.register(SequencingRunType, JsonEnumHandler)

class AssayStructureError(BaseException):
    def __init__(self, message, status_code=2):
        super().__init__(message)
        self.status_code = status_code

    def __str__(self):
        if self.status_code:
            return f"{self.status_code}: {self.args[0]}"
        return str(self.args[0])


# TODO complete this
# Translation mapping between STOCKS and EFO labels for protocols
STOCKS_PROTOCOL_TYPE_TO_EFO = {
    "LIBRARY_PREPARATION": ["nucleic acid library construction protocol", "EFO_0004184"],
    "CULTURE_GROWTH": ["growth protocol", "EFO_0005518"],
    "EXTRACTION": ["nucleic acid extraction protocol", "EFO_0002944"],
    "MOLECULAR_BIOLOGY": ["Other", "NA"],
    "SEQUENCING": ["nucleic acid sequencing protocol", "EFO_0004170"],
    "FIXATION": ["Other", "NA"]
}
