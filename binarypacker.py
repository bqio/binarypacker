from struct import pack as pk
from binarytypes import *
from pathlib import Path

import sys, inspect

def get_types() -> tuple:
    _types = inspect.getmembers(sys.modules["binarytypes"], inspect.isclass)
    out = ()
    for _type in _types:
        out += (_type[1],)
    return out

def parse_format(obj: object) -> str:
    out = ""
    for field_name in obj.__class__.__annotations__:
        field = obj.__class__.__annotations__[field_name]
        if isinstance(field, get_types()):
            if type(field) == type(UTF8String):
                _str = obj.__dict__[field_name]
                out += str(len(_str.encode('utf-8'))) + str(field)
            else:
                out += str(field)
        else:
            out += parse_format(obj.__getattribute__(field_name))
    return out

def _pack(obj: object) -> tuple:
    buf = ()
    for key in obj.__dict__:
        field = obj.__dict__[key]
        if issubclass(type(field), BinaryModel):
            buf += _pack(field)
        else:
            if isinstance(field, str):
                buf += (field.encode('utf-8'),)
            else:
                buf += (field,)
    return buf

def prepare_pack(obj: object, fmt: str) -> bytes:
    buf = _pack(obj)
    print(buf, fmt)
    return pk(fmt, *buf)

class BinaryModel:
    def get_format(self) -> str:
        return parse_format(self)
    
    def packBig(self) -> bytes:
        return prepare_pack(self, ">" + self.get_format())
    
    def packLittle(self) -> bytes:
        return prepare_pack(self, "<" + self.get_format())
    
    def dumpLittle(self, out_path: Path) -> None:
        with open(out_path, "wb") as fp:
            fp.write(self.packLittle())

    def dumpBig(self, out_path: Path) -> None:
        with open(out_path, "wb") as fp:
            fp.write(self.packBig())