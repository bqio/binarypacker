from dataclasses import dataclass, fields
from struct import pack, unpack, calcsize, error as struct_error
from typing import TypeVar, Type

from .types import *
from .endian import *

T = TypeVar('T', bound='SerializableObject')

def expand(cls=None, string_length_t = UInt8, string_encoding = "utf-8"):
    def wrap(cls):
        setattr(cls, "string_length_t", string_length_t)
        setattr(cls, "string_encoding", string_encoding)
        return cls
    if cls is None:
        return wrap
    return wrap(cls)

def get_nt_string_length(buf: bytes):
    len = 0
    for b in buf:
        if b == 0:
            break
        len += 1
    return len

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
            elif issubclass(field_type, str_types):
                # TODO
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
                if issubclass(field_type, String):
                    encoding = self.string_encoding if hasattr(self, "string_encoding") else "utf-8"
                    encoded_str = field_value.encode(encoding)
                    encoded_str_len = len(encoded_str)
                    fmt = self.string_length_t.fmt() if hasattr(self, "string_length_t") else "B"
                    serialized_data.extend(pack(f"{endian()}{fmt}", encoded_str_len))
                    serialized_data.extend(encoded_str)
                elif issubclass(field_type, NTString):
                    encoding = self.string_encoding if hasattr(self, "string_encoding") else "utf-8"
                    encoded_str = field_value.encode(encoding) + b'\x00'
                    serialized_data.extend(encoded_str)
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
            elif issubclass(field_type, String):
                try:
                    encoding = cls.string_encoding if hasattr(cls, "string_encoding") else "utf-8"
                    size_fmt = cls.string_length_t.fmt() if hasattr(cls, "string_length_t") else "B"
                    ssize = calcsize(size_fmt)
                    size = unpack(f"{endian()}{size_fmt}", serialized_data[offset:offset+ssize])[0]
                    offset += ssize
                    encoded_str = unpack(f"{endian()}{size}s", serialized_data[offset:offset+size])[0]
                    decoded_str = encoded_str.decode(encoding)
                    offset += size
                    setattr(instance, field_name, decoded_str)
                except struct_error:
                    raise TypeError("Check endian in both functions.")
            elif issubclass(field_type, NTString):
                encoding = cls.string_encoding if hasattr(cls, "string_encoding") else "utf-8"
                size = get_nt_string_length(serialized_data)
                encoded_str = unpack(f"{endian()}{size}s", serialized_data[offset:offset+size])[0]
                decoded_str = encoded_str.decode(encoding)
                offset += size + 1
                setattr(instance, field_name, decoded_str)
            else:
                fmt = f"{endian()}{field_type.fmt()}"
                size = calcsize(fmt)
                field_value = unpack(fmt, serialized_data[offset:offset+size])[0]
                offset += size
                setattr(instance, field_name, field_type(field_value))
        return instance