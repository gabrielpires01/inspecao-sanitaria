from enum import Enum


class RoleEnum(Enum):
    superuser = 1, "superuser"
    inspector = 2, "inspector"


class Status(Enum):
    authorized = 1, "authorized"
    has_irregularities = 2, "has_irregularities"
    finalized = 3, "finalized"
    finalized_prohibition = 4, "finalized_prohibition"
    finalized_partial_prohibition = 4, "finalized_partial_prohibition"
