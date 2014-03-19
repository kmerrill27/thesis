C_OUT = "./stackviz"

RUN_SCRIPT = "gdb -x {0} {1}"
C_COMPILE_ARGS = ["gcc", "-g", "ARG1", "-o", "ARG2"]
C_COMPILE = "gcc -g {0} -o {1}"

ARG1 = "ARG1"
ARG2 = "ARG2"

ASSEMBLY_START = "=>"

DISAS_IFILE = "./../gdb/disassemble.gdb"
DISAS_OFILE = "./../txt/disassemble.txt"
SCRIPT_FILE = "./../gdb/script.gdb"
INIT_FILE = "./../gdb/init.gdb"
LOG_FILE = "./../txt/log.txt"

NOT_C_SOURCE = "ERROR: not a C source file"
TITLE = "StackViz"
ARROW_ICON = "./../static/arrow.png"
STACK_ICON = "./../static/stack.png"

BASH_PROMPT = "\$"
GDB_PROMPT = "(gdb)"
OUTPUT_REDIRECT = "Redirecting output to {0}"
GDB_INIT_CMD = "gdb -x {0} {1}"
REMOVE_BR = "clear"
RUN = "run"
CONTINUE = "continue"
LINE_STEP = "step"
FUNCTION_STEP = "finish"
SET_LOG_FILE = "set logging file {0}"
SET_LOG_ON = "set logging on"
VAL_AT_ADDR = "x/x {0}"
INFO_SCOPE = "info scope {0}"
SRC_LINE = "info line"

BASE_POINTERS = ["rbp", "ebp"]
STACK_POINTERS = ["rip", "eip"]

ADDR_REGEX = "[0-9a-zA-Z]+:\s(.*)"
LEVEL_REGEX = ".*[.|\s]*Stack level ([0-9])+"
FUNCTION_REGEX = ".*\s*rip\s*=.*in\s+([0-9a-zA-Z]+)"
LINE_REGEX = ".*\.c:([0-9]+)\);"
SAVED_REG_REGEX = ".*Saved registers:\s*(.*)"
REG_ADDR_REGEX = "([a-zA-Z]{3})\sat\s(0x[0-9a-zA-Z]*)$"
SYMBOL_REGEX = ".*Symbol\s([0-9a-zA-Z]*).*offset\s0\+([-|0-9]*),"
LINE_NUM_REGEX = "Line\s([0-9]*)"
