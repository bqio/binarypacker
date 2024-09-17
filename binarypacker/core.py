from dataclasses import dataclass, fields
from struct import pack, unpack, calcsize
from typing import TypeVar, Type

from .types import *
from .endian import *

T = TypeVar('T', bound='SerializableObject')

@dataclass
class SerializableObject(object):
    def __post_init__(self) -> None:
        for field in fields(self):
            field_type = field.type
            field_name = field.name
            field_value = getattr(self, field_name)

            if issubclass(field_type, SerializableObject):
                field_value.__post_init__()
            elif issubclass(field_type, num_types):
                setattr(self, field_name, field_type(field_value))
            else:
                raise TypeError(f"Unknown type `{field_type}` on field `{field_name}`. Use only library types.\nMaybe you forgot @dataclass decorator or inheritance SerializableObject on `{field_type}`.")
    
    def serialize(self, endian: Endian = LittleEndian) -> bytes:
        serialized_data = bytearray()
        for field in fields(self):
            field_type = field.type
            field_name = field.name
            field_value = getattr(self, field_name)
            
            if issubclass(field_type, SerializableObject):
                serialized_data.extend(field_value.serialize(endian))
            else:
                field_fmt = f"{endian()}{field_type.fmt()}"
                serialized_data.extend(pack(field_fmt, field_value))
        return bytes(serialized_data)
    
    @classmethod
    def fmt(cls) -> str:
        fmt = ""
        for field in fields(cls):
            field_type = field.type
            fmt += field_type.fmt()
        return fmt

    @classmethod
    def deserialize(cls: Type[T], serialized_data: bytes, endian: Endian = LittleEndian) -> T:
        instance = cls.__new__(cls)
        offset = 0
        for field in fields(cls):
            field_type = field.type
            field_name = field.name

            if issubclass(field_type, SerializableObject):
                fmt = f"{endian()}{field_type.fmt()}"
                size = calcsize(fmt)
                field_value = field_type.deserialize(serialized_data[offset:offset+size], endian)
                offset += size
                setattr(instance, field_name, field_value)
            else:
                fmt = f"{endian()}{field_type.fmt()}"
                size = calcsize(fmt)
                field_value = unpack(fmt, serialized_data[offset:offset+size])[0]
                offset += size
                setattr(instance, field_name, field_type(field_value))
        return instance