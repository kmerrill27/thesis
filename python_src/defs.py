# Compile constants
C_OUT = "./stackexplorer"
C_COMPILE = "gcc -g {0} -o {1}"


# Display constants
BUTTON_WIDTH = 75
CURSOR_SIZE = 24
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600

WINDOWS = "Windows"

APP_TITLE = "StackExplorer"
ASSEMBLY_WIDGET_TITLE = "Assembly Code"
FRAME_WIDGET_TITLE = "Stack Frame"
SOURCE_WIDGET_TITLE = "Source Code"
STACK_WIDGET_TITLE = "Call Stack"

REVERSE_BUTTON_LABEL = "Flip stack"
LINE_STEP_LABEL = "Line step"
FUNCTION_STEP_LABEL = "Function step"
RUN_LABEL = "Run"
RESET_LABEL = "Reset"
HEX_MODE = "Hexadecimal"
DECIMAL_MODE = "Decimal"
ZOOM_MODE = "Zoom value"

# On Mac OS X, Ctrl corresponds to Command key
LINE_STEP_SHORTCUT = "Right"
FUNCTION_STEP_SHORTCUT = "Ctrl+Right"
RUN_SHORTCUT = "Space"
RESET_SHORTCUT = "Ctrl+Left"

BASE_POINTERS = ["ebp", "rbp"]
STACK_POINTERS = ["esp", "rsp"]
INSTR_POINTERS = ["eip", "rip"]

CALLER_SAVED = "Caller"
RETURN_ADDRESS = "Return address"
FRAME_BOTTOM = "Frame bottom: "
HEADER_BLANK = "					"
CARET = "^ "
DOWN_CARET = "v "
MAIN = "main"

RETURNED_VOID = "Function returned void."
RETURNED_WITH = "Function returned {0}."
PROGRAM_FINISHED = "Program exited {0}."

SELECT_FILE_MESSAGE = "Select a C source file"
LOAD_SOURCE_MESSAGE = "Load source"
NO_SOURCE_FILE = "No source file"
NOT_C_SOURCE = "ERROR: not a C source file"

STACK_ICON = "./../static/stack.png"
LINE_ICON = "./../static/arrow.png"
FUNCTION_ICON = "./../static/double_arrow.png"
RUN_ICON = "./../static/run.png"
RESET_ICON = "./../static/reset.png"
HEX_ICON = "./../static/hex.png"
DECIMAL_ICON = "./../static/ten.png"
ZOOM_ICON = "./../static/inspect.png"
UP_ICON = "./../static/up.png"
DOWN_ICON = "./../static/down.png"

NULL_VAL = 0
UNINITIALIZED = "null"
NON_STRUCT = ""
