class Int8(int):
    """Represents an 8-bit signed integer."""
    @classmethod
    def fmt(cls) -> str:
        return 'b'

class UInt8(int):
    """Represents an 8-bit unsigned integer."""
    @classmethod
    def fmt(cls) -> str:
        return 'B'

class Int16(int):
    """Represents a 16-bit signed integer."""
    @classmethod
    def fmt(cls) -> str:
        return 'h'

class UInt16(int):
    """Represents a 16-bit unsigned integer."""
    @classmethod
    def fmt(cls) -> str:
        return 'H'

class Int32(int):
    """Represents a 32-bit signed integer."""
    @classmethod
    def fmt(cls) -> str:
        return 'i'

class UInt32(int):
    """Represents a 32-bit unsigned integer."""
    @classmethod
    def fmt(cls) -> str:
        return 'I'

class Int64(int):
    """Represents a 64-bit signed integer."""
    @classmethod
    def fmt(cls) -> str:
        return 'q'

class UInt64(int):
    """Represents a 64-bit unsigned integer."""
    @classmethod
    def fmt(cls) -> str:
        return 'Q'

class String(str):
    """Represents a variable-length string."""
    @classmethod
    def fmt(cls) -> str:
        return 's'

class NTString(str):
    """Represents a null-terminated string."""
    @classmethod
    def fmt(cls) -> str:
        return 's'

num_types = (Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64)
str_types = (String, NTString)