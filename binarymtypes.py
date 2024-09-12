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