# Constants for GDB commands

# Pexpect values
BASH_PROMPT = "\$"
GDB_PROMPT = "\(gdb\)"


# Gdb constants
GDB_INIT_SCRIPT = "./../gdb/init.gdb"
MAIN = "main"

GDB_INIT_CMD = "gdb -x {0} {1}"
RUN = "run"
CONTINUE = "continue"
LINE_STEP = "step"
FUNCTION_STEP = "finish"

BREAK_ADDR = "break *{0}"
ENABLE_BREAKPOINT = "enable {0}"
DISABLE_ALL_BREAKPOINTS = "disable"
INSTR_AT_ADDR = "x/i {0}"
CARRIAGE_RETURN = ""

INFO_TARGET = "info target"
INFO_FUNCTIONS = "info functions"
INFO_LINE = "info line"
INFO_FRAME = "info frame"
INFO_ARGS = "info args"
INFO_LOCALS = "info locals"
INFO_ADDRESS = "info address {0}"

DISAS_LINE = "disassemble {0}, {1}"
DISAS_FUNCTION = "disas {0}"

PRINT_VAR = "print {0}"
PRINT_POINTER = "print *{0}"
PRINT_REGISTER = "print ${0}"
SIZEOF = "p sizeof({0})"

LAST_FRAME = "up"
NEXT_FRAME = "down"