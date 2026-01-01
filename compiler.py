from collections import Counter
from lexer import tokenize, token_patterns
from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator
from optimizer import CodeOptimizer
from register_allocator import RegisterAllocator
from target_codegen import TargetCodeGenerator

# ---------------- FILE PATHS ----------------
input_file = "test.mini"
tokens_file = "tokens.txt"
symbol_table_file = "symbol_table.txt"
reg_file = "reg.txt"
semantic_file = "semantic_analysis.txt"
ir_file = "ir.txt"
python_file = "output.py"
lexical_errors_file = "lexical_errors.txt"
clean_source_file = "clean_source.mini"
token_stats_file = "token_stats.txt"

# ---------------- READ SOURCE ----------------
with open(input_file, "r") as f:
    code = f.read()

# ---------------- LEXICAL ANALYSIS ----------------
tokens_list, lexical_errors, clean_code = tokenize(code)

with open(clean_source_file, "w") as f:
    f.write(clean_code)

with open(lexical_errors_file, "w") as f:
    if lexical_errors:
        f.write("Lexical Errors:\n")
        f.write("\n".join(lexical_errors))
    else:
        f.write("No lexical errors detected.\n")

# ---------------- TOKEN STREAM & SYMBOL TABLE ----------------
symbol_table = {}

with open(tokens_file, "w") as tf:
    for tok_type, tok_value, tok_line, tok_col in tokens_list:
        tf.write(f"<{tok_line}, {tok_col}> <{tok_type}, {tok_value}>\n")

        if tok_type in [
            "IDENTIFIER",
            "INTEGER_LITERAL",
            "FLOAT_LITERAL",
            "CHAR_LITERAL",
            "STRING_LITERAL",
        ]:
            if tok_value not in symbol_table:
                symbol_table[tok_value] = {
                    "type": tok_type.lower().replace("_literal", ""),
                    "category": "variable" if tok_type == "IDENTIFIER" else "literal",
                    "line": tok_line,
                    "column": tok_col,
                }

# ---------------- TOKEN STATISTICS ----------------
counts = Counter(t[0] for t in tokens_list)

with open(token_stats_file, "w") as f:
    f.write("Token Type           Count\n")
    f.write("-------------------------\n")
    for token, count in counts.items():
        f.write(f"{token.ljust(20)} {count}\n")

# ---------------- SEMANTIC ANALYSIS ----------------
analyzer = SemanticAnalyzer()
semantic_errors = []

i = 0
while i < len(tokens_list):

    tok_type, tok_value, tok_line, _ = tokens_list[i]

    # ---------------- DECLARATIONS ----------------
    if tok_type in ["INT", "FLOAT", "CHAR"] and i + 1 < len(tokens_list):
        next_type, next_value, next_line, _ = tokens_list[i + 1]

        # Ignore function declaration like: int main()
        if next_type == "IDENTIFIER":
            # Check if next next token is '(' → function
            if i + 2 < len(tokens_list) and tokens_list[i + 2][1] == "(":
                i += 1
                continue

            try:
                analyzer.declare(next_value, tok_type.lower(), next_line)
            except Exception as e:
                semantic_errors.append(f"Line {next_line}: {e}")

    # ---------------- ASSIGNMENTS ----------------
    if tok_type == "OPERATOR" and tok_value == "=":

        lhs = tokens_list[i - 1][1]

        # Collect full RHS expression until ';'
        expr_tokens = []
        j = i + 1
        while j < len(tokens_list) and tokens_list[j][1] != ";":
            expr_tokens.append(tokens_list[j][1])
            j += 1

        expr_str = " ".join(expr_tokens)

        # Determine type only if single literal
        type_map = {
            "INTEGER_LITERAL": "int",
            "FLOAT_LITERAL": "float",
            "CHAR_LITERAL": "char",
            "STRING_LITERAL": "string",
        }

        rhs_type = (
            type_map.get(tokens_list[i + 1][0])
            if len(expr_tokens) == 1
            else None
        )

        try:
            analyzer.assign(lhs, expr_str, rhs_type, tok_line)
        except Exception as e:
            semantic_errors.append(f"Line {tok_line}: {e}")

        i = j
        continue

    i += 1

# ---------------- WRITE SEMANTIC OUTPUT ----------------
with open(semantic_file, "w") as f:
    if semantic_errors:
        f.write("Semantic Errors:\n")
        f.write("\n".join(semantic_errors))
    else:
        f.write("No semantic errors detected.\n")

analyzer.write_symbol_table(symbol_table_file)


# ---------------- REGEX / TOKEN PATTERNS ----------------
examples = {
    "IDENTIFIER": "counter, _var2",
    "INTEGER_LITERAL": "123",
    "FLOAT_LITERAL": "3.14",
    "CHAR_LITERAL": "'a'",
    "STRING_LITERAL": '"hello"',
    "OPERATOR": "+, -, *, /, =",
    "SYMBOL": ";, (, )",
    "KEYWORD": "int, float, char",
}

token_col_width = max(len(k) for k in token_patterns) + 4
pattern_col_width = max(len(v) for v in token_patterns.values()) + 4

with open(reg_file, "w") as rf:
    rf.write(
        f"{'Token Type'.ljust(token_col_width)}"
        f"{'Regex / Pattern'.ljust(pattern_col_width)}"
        f"Example\n"
    )
    for tok, pat in token_patterns.items():
        rf.write(
            f"{tok.ljust(token_col_width)}"
            f"{pat.ljust(pattern_col_width)}"
            f"{examples.get(tok, '')}\n"
        )

# ---------------- IR GENERATION ----------------
codegen = CodeGenerator()
temp_count = 1

for i, (tok_type, tok_value, _, _) in enumerate(tokens_list):

    if tok_type == "OPERATOR" and tok_value == "=":
        lhs = tokens_list[i - 1][1]

        # Arithmetic expression
        if i + 3 < len(tokens_list) and tokens_list[i + 2][0] == "OPERATOR":
            op1 = tokens_list[i + 1][1]
            operator = tokens_list[i + 2][1]
            op2 = tokens_list[i + 3][1]

            temp = f"t{temp_count}"
            temp_count += 1

            codegen.generate_expression(temp, op1, operator, op2)
            codegen.generate_assignment(lhs, temp)

        else:
            rhs = tokens_list[i + 1][1]
            codegen.generate_assignment(lhs, rhs)

codegen.write_output()

# ---------------- OPTIMIZATION ----------------
optimizer = CodeOptimizer(ir_file="ir.txt", optimized_file="optimized_ir.txt")
optimizer.optimize()
optimizer.write_optimized_ir()

# ---------------- REGISTER ALLOCATION ----------------
allocator = RegisterAllocator(ir_file="optimized_ir.txt", reg_file="reg_ir.txt")
allocator.allocate()
allocator.write_register_ir()

# ---------------- TARGET CODE GENERATION ----------------
target = TargetCodeGenerator(
    ir_file="optimized_ir.txt",
    target_file="target_code.txt",
)
target.generate()
target.write_target_code()

# ---------------- FINAL OUTPUT ----------------
print("Lexical, semantic analysis, and code generation completed!")
print(f"Tokens saved to {tokens_file}")
print(f"Symbol table saved to {symbol_table_file}")
print(f"Semantic analysis saved to {semantic_file}")
print(f"Lexical errors saved to {lexical_errors_file}")
print(f"Clean source saved to {clean_source_file}")
print(f"Regular expressions saved to {reg_file}")
print(f"Token statistics saved to {token_stats_file}")
print(f"IR code saved to {ir_file} and Python code saved to {python_file}")
print("Target code generation completed!")
