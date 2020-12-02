# PyARMv8
* Turing complete ARMv8 processor and assembler implemented in pure Python3.
* To execute the processor/assembler, run "python3 Assembler.py <armv8_assembly_file>" in terminal.
* I have provided an example test.S file for reference.

## Supported Instructions
* Register Type Instructions
** ADD
** SUB
** AND
** ORR
* Immediate Type Instructions
** ADD
** SUB
* Data Type Instructions
** LDUR
** STUR
* Conditional Branch Type Instructions
** CBZ
* Unconditional Branch Type Instructions
** B

## Other Notes on Usage
* Tags are supported for usage in CB and B instructions. However, tags are currently only supported using the syntax present in "test.S". The tag should be in the form "<tag_name>:\n"
