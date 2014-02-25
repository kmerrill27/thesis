# In GDB: python execfile ("test.py")

import sys
import gdb

gdb.execute("file fact_rec")
br1 = gdb.Breakpoint("1")
br2 = gdb.Breakpoint("factorial")
gdb.execute("run")
