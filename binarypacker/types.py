class Int8Meta(type):
    def __str__(self) -> str:
        return "b"

class UInt8Meta(type):
    def __str__(self) -> str:
        return "B"

class Int16Meta(type):
    def __str__(self) -> str:
        return "h"

class UInt16Meta(type):
    def __str__(self) -> str:
        return "H"

class Int32Meta(type):
    def __str__(self) -> str:
        return "l"

class UInt32Meta(type):
    def __str__(self) -> str:
        return "L"
    
class Int64Meta(type):
    def __str__(self) -> str:
        return "q"

class UInt64Meta(type):
    def __str__(self) -> str:
        return "Q"

class UTF8StringMeta(type):
    def __str__(self) -> str:
        return "s"

class Int8(metaclass=Int8Meta):
    pass

class UInt8(metaclass=UInt8Meta):
    pass

class Int16(metaclass=Int16Meta):
    pass

class UInt16(metaclass=UInt16Meta):
    pass

class Int32(metaclass=Int32Meta):
    pass

class UInt32(metaclass=UInt32Meta):
    pass

class Int64(metaclass=Int64Meta):
    pass

class UInt64(metaclass=UInt64Meta):
    pass

class UTF8String(metaclass=UTF8StringMeta):
    pass