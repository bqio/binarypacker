from struct import pack as pk
from .types import *
from pathlib import Path

import sys, inspect

class BinaryModel:
    def __get_types(self) -> tuple:
        types = inspect.getmembers(sys.modules["binarypacker.types"], inspect.isclass)
        out = ()
        for type in types:
            out += (type[1],)
        return out

    def __parse_format(self, obj: object) -> str:
        out = ""
        for field_name in obj.__class__.__annotations__:
            field = obj.__class__.__annotations__[field_name]
            if isinstance(field, self.__get_types()):
                if type(field) == type(UTF8String):
                    _str = obj.__dict__[field_name]
                    out += str(len(_str.encode('utf-8'))) + str(field)
                else:
                    out += str(field)
            else:
                out += self.__parse_format(obj.__getattribute__(field_name))
        return out

    def __prepare_pack(self, obj: object, fmt: str) -> bytes:
        buf = self.__pack(obj)
        return pk(fmt, *buf)
    
    def __pack(self, obj: object) -> tuple:
        buf = ()
        for key in obj.__dict__:
            field = obj.__dict__[key]
            if issubclass(type(field), BinaryModel):
                buf += self.__pack(field)
            else:
                if isinstance(field, str):
                    buf += (field.encode('utf-8'),)
                else:
                    buf += (field,)
        return buf
    
    def get_format(self) -> str:
        return self.__parse_format(self)
    
    def packBig(self) -> bytes:
        return self.__prepare_pack(self, ">" + self.get_format())
    
    def packLittle(self) -> bytes:
        return self.__prepare_pack(self, "<" + self.get_format())
    
    def dumpLittle(self, out_path: Path) -> None:
        with open(out_path, "wb") as fp:
            fp.write(self.packLittle())

    def dumpBig(self, out_path: Path) -> None:
        with open(out_path, "wb") as fp:
            fp.write(self.packBig())