import enum


class TripAssignmentStatus(str, enum.Enum):
    accepted = "accepted"
    rejected = "rejected"


class TripEventType(str, enum.Enum):
    pick_up = "pick-up"
    drop_off = "drop-off"
