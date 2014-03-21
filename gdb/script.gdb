# Get assembly code for given line number

set confirm off
set disassemble-next-line on
set logging overwrite on
set logging redirect on
set logging file ./../txt/disassemble.txt
break 48
set logging on
run
set logging off