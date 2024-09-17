class Endian:
    pass

class BigEndian(Endian):
    def __str__(self) -> str:
        return ">"

class LittleEndian(Endian):
    def __str__(self) -> str:
        return "<"