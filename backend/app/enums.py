from enum import IntEnum


class RoleEnum(IntEnum):
    superuser = 1
    inspector = 2


class Status(IntEnum):
    clear = 1
    has_irregularities = 2
    immediate_prohibition = 3
    finalized = 4
    finalized_prohibition = 5
    finalized_partial_prohibition = 6


class Severity(IntEnum):
    low = 1
    moderate = 2
    major = 3
    critical = 4
    resolved = 5


class FinalizeStatus(IntEnum):
    accordingly = 1
    with_problems = 2
    partial_prohibition = 3
    prohibition = 4
