from enum import Enum


class BatchStatus(Enum):
    UNKNOWN = "UNKNOWN"
    INVALID = "INVALID"
    PENDING = "PENDING"
    COMMITTED = "COMMITTED"
