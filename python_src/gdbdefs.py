# Constants for GDB commands

# Pexpect values
BASH_PROMPT = "\$"
GDB_PROMPT = "\(gdb\)"


# Gdb constants
GDB_INIT_SCRIPT = "./../gdb/init.gdb"

GDB_INIT_CMD = "gdb -x {0} {1}"
RUN = "run"
CONTINUE = "continue"
LINE_STEP = "step"
FUNCTION_STEP = "finish"

BREAK_ADDR = "break *{0}"
REMOVE_BR = "del"

INFO_TARGET = "info target"
INFO_LINE = "info line"
INFO_FRAME = "info frame"
INFO_ARGS = "info args"
INFO_LOCALS = "info locals"
INFO_ADDRESS = "info address {0}"

DISAS = "disassemble {0}, {1}"
DISAS_MAIN = "disas main"

PRINT_VAR = "print {0}"
PRINT_POINTER = "print *{0}"
PRINT_REGISTER = "print ${0}"
SIZEOF = "p sizeof({0})"

LAST_FRAME = "up"
NEXT_FRAME = "down"