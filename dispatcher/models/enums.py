import enum


class TaxiStatus(str, enum.Enum):
    available = "available"
    busy = "busy"
    off = "off"


class TripRequestStatus(str, enum.Enum):
    taxi_assigned = "taxi_assigned"
    no_taxi_available = "no_taxi_available"
    error_during_assigning = "error_during_assigning"
