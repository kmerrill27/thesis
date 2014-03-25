C_OUT = "./stackviz"

RUN_SCRIPT = "gdb -x {0} {1}"
C_COMPILE_ARGS = ["gcc", "-g", "ARG1", "-o", "ARG2"]
C_COMPILE = "gcc -g {0} -o {1}"

ASSEMBLY_START = "=>"
UNINITIALIZED = "null"
CALLEE_SAVED = "Callee"
RETURN_ADDRESS = "Return address"
PROGRAM_FINISHED = "Program exited {0}."
RETURNED_VOID = "Function returned void."
RETURNED_WITH = "Function returned {0}."
ASSEMBLER_DUMP = "End of assembler dump."
DUMP_OF_ASSEMBLY = "Dump of assembler code from"

INIT_FILE = "./../gdb/init.gdb"

NOT_C_SOURCE = "ERROR: not a C source file"
TITLE = "StackExplorer"
ARROW_ICON = "./../static/arrow.png"
STACK_ICON = "./../static/stack.png"

BASH_PROMPT = "\$"
GDB_PROMPT = "\(gdb\)"
RETURN_TO_CONTINUE = "---Type <return> to continue, or q <return> to quit---"
IN_MAIN = "\"finish\" not meaningful in the outermost frame."
GDB_INIT_CMD = "gdb -x {0} {1}"
REMOVE_BR = "del"
RUN = "run"
CONTINUE = "continue"
LINE_STEP = "step"
FUNCTION_STEP = "finish"
SOURCE = "source {0}"
VAL_AT_ADDR = "x/{0}x {1}"
INFO_SCOPE = "info scope {0}"
SRC_LINE = "info line"
SRC_LINE_AT_ADDR = "info line *{0}"
INFO_FRAME = "info frame"
INFO_LOCALS = "info locals"
INFO_ARGS = "info args"
INFO_TARGET = "info target"
REG_VAL = "x/x ${0}"
PRINT_SYMBOL = "print {0}"
PRINT_REGISTER = "print ${0}"
LAST_FRAME = "up"
NEXT_FRAME = "down"
DISAS = "disassemble {0}, {1}"
DISAS_MAIN = "disas main"
BREAK_ADDR = "break *{0}"

BASE_POINTERS = ["ebp", "rbp"]
STACK_POINTERS = ["esp", "rsp"]
INSTR_POINTERS = ["eip", "rip"]

ARCH_REGEX = "file type mach-o-x86-([0-9]*)"
VAR_REGEX = "([a-zA-Z0-9_-]*)\s=\s(.*\s*)"
PTR_REGEX = "([0-9a-zA-Z]+):\s.*"
ADDR_REGEX = "[0-9a-zA-Z]+:\s(.*)"
LEVEL_REGEX = ".*[.|\s]*Stack level ([0-9])+"
BOTTOM_REGEX = "[.|\s]*Stack level [0-9]+, frame at ([0-9a-zA-Z]*):"
FUNCTION_REGEX = "rip\s*=.*in\s+([0-9a-zA-Z\_\-]+)"
LINE_REGEX = "\.c:([0-9]+)\);"
SAVED_REG_REGEX = ".*Saved registers:\s*(.*)"
REG_ADDR_REGEX = "\s([a-zA-Z]{3})\sat\s(0x[0-9a-zA-Z]*)"
SYMBOL_REGEX = "Symbol\s([0-9a-zA-Z_-]*).*offset\s0\+([-|0-9]*),\slength\s([0-9]*)"
LINE_NUM_REGEX = "Line\s([0-9]*)"
LINE_NUM_AND_ASSEMBLY_REGEX = "Line\s([0-9]*).*starts at address ([0-9a-zA-Z]*).*\s*and ends at ([0-9a-zA-Z]*)"
PRINT_REGEX = "[0-9]*\s=\s(.*)"
PRINT_SAVED_REGISTER_REGEX = "\$[0-9]*\s=\s(\(void.*)"
PRINT_REGISTER_REGEX = "[0-9]*\s=\s\(void \*\)\s(.*)"
RETURN_REGEX = "Value\sreturned\sis\s\$[0-9]*\s=\s([0-9a-zA-Z]*)"
BREAKPOINT_REGEX = "Breakpoint [0-9]*,"
BREAKPOINT_HIT_REGEX = "Breakpoint ([0-9]*),"
EXIT_REGEX = "exited (.*)]"
POP_ADDR_REGEX = "([0-9a-zA-Z]*)\s<.*>:\spop.*\s.*retq"
BREAKPOINT_NUM_REGEX = "Breakpoint\s([0-9]*)\sat"
RETURN_ADDRESS_REGEX = "\s(0x[0-9a-zA-Z]*)\s"

NULL_VAL = 0
SIZEOF = "p sizeof({0})"
INFO_ADDRESS = "info address {0}"
PRINT_VAR = "print {0}"
PRINT_POINTER = "print *{0}"
ADDRESS_REGEX = "Symbol.*offset\s0\+([-|0-9]*)."
VAL_REGEX = "\$[0-9]*\s=\s(.*)"
VAR_NAME_REGEX = "([a-zA-Z0-9_-]*)\s="
STRUCT_REGEX = "(\(struct .* \*\))\s(0x[0-9a-zA-Z]*)"
NON_STRUCT = ""
