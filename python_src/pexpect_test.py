#!/usr/bin/env python
'''This starts the python interpreter; captures the startup message; then gives the user interactive control over the session.
Why?
'''

# Don't do this unless you like being John Malkovich
# c = pexpect.spawn ('/usr/bin/env python ./python.py')

import pexpect
import re
from defs import *

c = pexpect.spawn ('/usr/bin/env python')
c.expect ('>>>')
print 'And now for something completely different...'
f = lambda s:s and f(s[1:])+s[0] # Makes a function to reverse a string.
print c.before
print 'Yes, it\'s python, but it\'s backwards.'
print
print 'Escape character is \'^]\'.'
print c.after
#c.interact()
c.kill(1)
print 'is alive:', c.isalive()

d = pexpect.spawn("ls")
d.expect("^.*$")
print "before: /", d.before, "/"
print "BETWEEN"
print "after: /", d.after, "/"
print 'is alive: ', d.isalive()

p = pexpect.spawn('bash')
p.expect("\$")
p.sendline('ls')  # For instance
p.expect("\$")
print(p.before)  # Get the output from the last command.

g = pexpect.spawn("bash")
g.expect("\$")
g.sendline("gdb stackviz")
g.expect("(gdb)")
print "before: /", g.before, "/"
print "after: /", g.after, "/"
print 'is alive: ', g.isalive()

g.sendline(GDB_INIT_CMD.format(INIT_FILE, C_OUT))
g.expect("(gdb)")
print "before: /", g.before, "/"
print "after: /", g.after, "/"
print 'is alive: ', g.isalive()

g.sendline("set confirm off")
g.expect("(gdb)")
g.sendline("set disassemble-next-line on")
g.expect("(gdb)")
print "1"
g.sendline("set logging overwrite on")
g.expect("(gdb)")
print "2"
g.sendline("set logging redirect on")
g.expect("(gdb)")
print "3"
g.sendline("set logging file ../txt/disassemble.txt")
g.expect("(gdb)")
print "4"
g.sendline("rbreak .")
g.expect("Breakpoint")
print "5"
g.sendline("set logging on")
g.expect("Redirecting output to ../txt/disassemble.txt.")
print "6"
g.sendline("run")
g.expect("(gdb)")
print "7"
g.sendline("del")
g.expect("(gdb)")
g.sendline("continue")
g.expect("(gdb)")
print "8"
print "before: /", g.before, "/"
print "after: /", g.after, "/"
#g.sendline("q")
#g.expect("\$")
print "before: /", g.before, "/"
print "after: /", g.after, "/"
print "9"
print 'is alive: ', g.isalive()
#g.close()
print 'is alive: ', g.isalive()


gdb_process = pexpect.spawn('bash')
gdb_process.expect(BASH_PROMPT)
print GDB_INIT_CMD.format(INIT_FILE, C_OUT)
gdb_process.sendline(GDB_INIT_CMD.format(INIT_FILE, C_OUT))
gdb_process.expect(GDB_PROMPT)
# Set up logging to file
#print SET_LOG_FILE.format(LOG_FILE)
#gdb_process.sendline(SET_LOG_FILE.format(LOG_FILE))
#gdb_process.expect(GDB_PROMPT)
#print RUN
gdb_process.sendline(RUN)
gdb_process.expect(GDB_PROMPT)
#print SET_LOG_ON
#gdb_process.sendline(SET_LOG_ON)
#gdb_process.expect(OUTPUT_REDIRECT.format(LOG_FILE))
gdb_process.sendline(CONTINUE)
gdb_process.expect(GDB_PROMPT)
gdb_process.sendline(FUNCTION_STEP)
gdb_process.expect(GDB_PROMPT)
bef = gdb_process.before.strip()
print bef
retval_match = re.search(RETURN_REGEX, bef)
if retval_match:
	retval = retval_match.group(1)
	print retval
print 'is alive: ', gdb_process.isalive()
