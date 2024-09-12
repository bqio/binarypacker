### BinaryPacker
Simple python binary packer.


#### Install
```bash
py -m venv env
env/Scripts/activate
pip install git+https://github.com/bqio/binarypacker.git
```


#### Usage
```python
from binarypacker.core import BinaryModel
from binarypacker.types import *

class Header(BinaryModel):
    flag: UInt8
    size: Int64
    offset: UInt32

class File(BinaryModel):
    data: Int32
    filename: UTF8String
    header: Header

file = File()
header = Header()

header.flag = 1
header.size = 2
header.offset = 16

file.data = 34
file.filename = "Hello"
file.header = header

print(file.get_format())
file.dumpLittle("data.dat")
```
#### Result
```
00000000: 22 00 00 00 48 65 6C 6C  6F 01 02 00 00 00 00 00  "...Hello.......
00000010: 00 00 10 00 00 00                                 ......
```