from enum import Enum
from sqlalchemy.types import Integer, TypeDecorator


class IntEnum(TypeDecorator):
    impl = Integer
    python_type = Integer
    is_enum_type = True

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def __repr__(self):
        return self.impl.__repr__()

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, Enum):
            return value.value
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        enum_dict = {v.value[0]: v.name for v in self._enumtype}
        try:
            return getattr(self._enumtype, enum_dict[value])
        except KeyError:
            raise ValueError(f"Invalid value for {self._enumtype.__name__}: {value}")
