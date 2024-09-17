### BinaryPacker/Unpacker
Simple python binary packer/unpacker.


#### Install
```bash
py -m venv env
env/Scripts/activate
pip install git+https://github.com/bqio/binarypacker.git
```


#### Usage
```python
from dataclasses import dataclass
from binarypacker.core import SerializableObject
from binarypacker.endian import BigEndian
from binarypacker.types import *

# @dataclass required
    
@dataclass
class Table(SerializableObject):
    ptr: Int8
    
@dataclass
class Header(SerializableObject):
    offset: Int16
    table: Table

@dataclass
class File(SerializableObject):
    header: Header
    age: Int8
    size: Int8

table = Table(ptr=120)
header = Header(offset=24, table=table)
file = File(header=header, age=2, size=8)

serialized_data = file.serialize(endian=BigEndian)

print(serialized_data)

file2 = File.deserialize(serialized_data)

print(file2.age, file2.size, type(file2.header.table.ptr))
```
#### Output
```
b'\x00\x18x\x02\x08'
2 8 <class 'binarypacker.types.Int8'>
```

### TODO

* Implement String and NTString serialization/deserialization