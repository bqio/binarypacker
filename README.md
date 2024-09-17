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
from binarypacker.core import SerializableObject, expand
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
@expand(string_length_t = UInt16)
class File(SerializableObject):
    # [string][nt] Default encoding utf-8. Use @expand on class for change string encoding.
    filename: NTString
    # [string_length][string] Max string length 255 bytes (uint8) in default. Use @expand on class for change length type.
    filename2: String
    header: Header
    age: Int8
    size: Int8

table = Table(ptr=120)
header = Header(offset=24, table=table)
file = File(filename="data.info", filename2="data2.dat", header=header, age=2, size=8)

# default LittleEndian
serialized_data = file.serialize(endian=BigEndian)

print(serialized_data)

file2 = File.deserialize(serialized_data, endian=BigEndian)

print(file.filename, file.filename2, file2.age, file2.size, type(file2.header.table.ptr))
```
#### Output
```
b'data.info\x00\x00\tdata2.dat\x00\x18x\x02\x08'
data.info data2.dat 2 8 <class 'binarypacker.types.Int8'>
```

### TODO

* ~~Implement String/NTString serialization/deserialization.~~
* Implement `List` types.