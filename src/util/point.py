from ctypes import *

class Point(Structure):
  _fields_ = [("x", c_long), ("y", c_long)]

