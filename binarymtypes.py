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