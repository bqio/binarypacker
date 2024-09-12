from binarypacker import BinaryModel
from binarytypes import *

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

file.dumpLittle("data.dat")