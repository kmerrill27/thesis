clear
disassemble main
# Get address at add before retq and pop
break *addr
continue
info locals
q