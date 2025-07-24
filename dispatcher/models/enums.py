import enum


class TaxiStatus(str, enum.Enum):
    available = "available"
    busy = "busy"
