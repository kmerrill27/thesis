# In GDB: python execfile ("test.py")
# From terminal: gdb -q -x test.py 

import sys
import gdb

gdb.execute("file stackviz")
br1 = gdb.Breakpoint("1")
br2 = gdb.Breakpoint("factorial")
gdb.execute("run")
