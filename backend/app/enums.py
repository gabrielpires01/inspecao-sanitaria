from enum import IntEnum


class RoleEnum(IntEnum):
    superuser = 1
    inspector = 2


class Status(IntEnum):
    clear = 1
    low = 2
    moderate = 3
    major = 4
    critical = 5
    finalized = 6
    finalized_prohibition = 7
    finalized_partial_prohibition = 8


class Severity(IntEnum):
    low = 1
    moderate = 2
    major = 3
    critical = 4
