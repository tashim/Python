#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  f1.py
#  
#  Copyright 2019 e_tas <e_tas@DESKTOP-8LF2SE6>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys
import os

filename = 'data.txt'
with open(filename, 'w') as fh:
    fh.write("Hello World!\nHow are you today?\nThank you!")
 
print(os.path.getsize(filename))  # 42
 
with open(filename,'a+') as fh:
    print(fh.tell())        # 0
    row = fh.readline()
    print(row)              # Hello World!
    print(fh.tell())        # 13
 
    print(fh.seekable())
    print(fh.tell())        # 6
 
    row = fh.readline()
    print(row)              # World!
    print(fh.tell())        # 13
 
    fh.seek(0, os.SEEK_SET)
    print(fh.tell())        # 0
    print(fh.read(5))       # Hello
 
    fh.seek(0, os.SEEK_END)
    print(fh.tell())        # 38
    print(fh.read())        # you!
    print(fh.tell())        # 42
