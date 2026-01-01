====================================
MINI LANGUAGE COMPILER – README
====================================

Project Title:
--------------
Mini Language Compiler using Python

Author:
-------
Sarmad Ali

Course:
-------
Compiler Construction

Description:
------------
This project implements a **Mini Language Compiler** using Python.  
It covers all the **major phases of a compiler**, from lexical analysis to target code generation.  

The compiler reads a source file written in a simplified **C-like language (.mini)** and produces several outputs, including **tokens, symbol table, intermediate code, optimized code, register-based code, and final target code**.  
This project is primarily designed for **learning and understanding compiler design** rather than full C language support.

------------------------------------
PROJECT DIRECTORY STRUCTURE
------------------------------------

.vscode/                  → VS Code settings  
__pycache__/              → Python cache files  
minlang-env/              → Python virtual environment  

Assignment 1.docx         → Project documentation  
notes.txt                 → Project notes  
task.txt                  → Task description  

Source Files:
-------------
compiler.py                → Main driver file  
lexer.py                   → Lexical analyzer  
parser.py                  → Syntax parser  
semantic_analyzer.py       → Semantic analysis & symbol table  
ir_generator.py            → Intermediate code generator  
code_generator.py          → IR code generation  
optimizer.py               → Intermediate code optimizer  
register_allocator.py      → Register allocation module  
target_codegen.py          → Target code generator  
cli.py                     → Command Line Interface (optional)  

Input File:
-----------
test.mini                  → Mini language source code for testing  
clean_source.mini          → Source code after removing comments  

Generated Output Files:
-----------------------
tokens.txt                 → List of tokens  
token_stats.txt            → Token statistics  
lexical_errors.txt         → Lexical error report  

symbol_table.txt           → Symbol table  
semantic_analysis.txt      → Semantic analysis results  

ir.txt                     → Intermediate representation (3-address code)  
optimized_ir.txt           → Optimized IR  
reg_ir.txt                 → Register-mapped IR  
target_code.txt            → Final target code  

reg.txt                    → Regex patterns used  
requirements.txt           → Project dependencies  
setup.py                   → Setup file  
output.py                  → Python-equivalent output (for testing)  

------------------------------------
SUPPORTED LANGUAGE FEATURES
------------------------------------
✔ int data type  
✔ Variable declaration  
✔ Assignment statements  
✔ Arithmetic expressions (+, -, *, /)  
✔ if statement  
✔ return statement  
✔ main() function  

------------------------------------
EXAMPLE INPUT (test.mini)
------------------------------------

int main() {
    int x = 5;
    int y = 10;
    int z = x + y;
    return z;
}

------------------------------------
COMPILER PHASES
------------------------------------

1. Lexical Analysis
   - File: lexer.py
   - Converts source code into **tokens**
   - Detects **lexical errors**

2. Syntax Analysis
   - File: parser.py
   - Validates **grammar rules**
   - Checks statements, expressions, and blocks

3. Semantic Analysis
   - File: semantic_analyzer.py
   - Builds **symbol table**
   - Checks **type compatibility** and variable declarations

4. Intermediate Code Generation
   - Files: ir_generator.py / code_generator.py
   - Produces **three-address code (TAC)**

5. Code Optimization
   - File: optimizer.py
   - Performs **constant folding**  
   - Removes **redundant instructions**

6. Register Allocation
   - File: register_allocator.py
   - Maps variables to **virtual registers**

7. Target Code Generation
   - File: target_codegen.py
   - Generates the **final target code**  

------------------------------------
HOW TO RUN THE COMPILER
------------------------------------

1. Activate Python virtual environment (if used)  
2. Open terminal in the project directory  
3. Run the compiler:  

   python compiler.py

4. Output files will be generated automatically in the project folder  

------------------------------------
LIMITATIONS
------------------------------------
- Only supports a single function (**main**)  
- No loops (**for / while**)  
- No arrays or pointers  
- Limited data types (int only)  

------------------------------------
FUTURE ENHANCEMENTS
------------------------------------
- Support for loops and multiple functions  
- Advanced function calls  
- Generate assembly-level code (MIPS / x86)  
- Enhanced optimization techniques  
- Improved error handling and recovery  

------------------------------------
CONCLUSION
------------------------------------
This project demonstrates a **complete compiler pipeline** from source code to target code.  
It provides hands-on experience and a solid foundation for understanding **compiler design and implementation concepts**.  

====================================
END OF README
====================================
