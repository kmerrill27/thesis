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
GDB_INIT_CMD = "gdb -x {0} {1}"
REMOVE_BR = "delete"
RUN = "run"
LINE_STEP = "step"
FUNCTION_STEP = "finish"
SET_LOG_FILE = "set logging file {0}"
SET_LOG_ON = "set logging on"