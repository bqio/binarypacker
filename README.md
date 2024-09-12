### BinaryPacker
Simple python binary packer.


#### Usage
```python
from binarypacker import BinaryModel
from binarytypes import *

class Header(BinaryModel):
    size: Int64
    offset: UInt32

class File(BinaryModel):
    data: Int32
    header: Header

file = File()
header = Header()

header.size = 2
header.offset = 16

file.data = 34
file.header = header

file.dumpLittle("data.dat")
```