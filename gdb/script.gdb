# Get assembly code for given line number

set disassemble-next-line on
set logging overwrite on
set logging redirect on
set logging file ../txt/disassemble.txt
break 23
set logging on
run
set logging off
q