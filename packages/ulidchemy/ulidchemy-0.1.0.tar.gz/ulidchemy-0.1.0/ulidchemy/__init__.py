import ulid
from sqlalchemy import text, types
from sqlalchemy.dialects.postgresql import BYTEA


ulid_default_func = text("gen_monotonic_ulid()")


class ULIDType(types.UserDefinedType):
    cache_ok = True

    def get_col_spec(self, **kw):
        return "ulid"

    def bind_processor(self, dialect):
        def process(value):
            if isinstance(value, ulid.ULID):
                return value.str  # Convert ULID to string
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                return ulid.parse(value)  # Convert string to ULID
            return value

        return process

    def python_type(self):
        return ulid.ULID
