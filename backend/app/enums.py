from enum import IntEnum


class RoleEnum(IntEnum):
    superuser = 1
    inspector = 2


class Status(IntEnum):
    authorized = 1
    has_irregularities = 2
    finalized = 3
    finalized_prohibition = 4
    finalized_partial_prohibition = 5
