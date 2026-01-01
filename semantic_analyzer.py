# semantic_analyzer.py
class SemanticAnalyzer:
    def __init__(self):
        """
        Symbol table structure:
        name → {
            type: data type (int, float, char, ...)
            scope: scope name (main for now)
            value: assigned value / temp register
            declared_at: declaration line number
            last_updated: last assignment line number
        }
        """
        self.symbols = {}
        self.current_scope = "main"

    def declare(self, name, vtype, lineno):
        """
        Declare a variable.
        """
        if name in self.symbols:
            raise Exception(
                f"Semantic Error (line {lineno}): Variable '{name}' already declared."
            )

        self.symbols[name] = {
            "type": vtype,
            "scope": self.current_scope,
            "value": None,
            "declared_at": lineno,
            "last_updated": None
        }

    def assign(self, name, value=None, vtype=None, lineno=None):
        """
        Assign a value to a variable.
        """
        if name not in self.symbols:
            raise Exception(
                f"Semantic Error (line {lineno}): Variable '{name}' not declared."
            )

        # Type checking
        if vtype and self.symbols[name]["type"] != vtype:
            raise Exception(
                f"Semantic Error (line {lineno}): Type mismatch for '{name}'. "
                f"Expected '{self.symbols[name]['type']}', got '{vtype}'."
            )

        self.symbols[name]["value"] = value
        self.symbols[name]["last_updated"] = lineno

    def lookup(self, name, lineno=None):
        """
        Lookup a variable in the symbol table.
        """
        if name not in self.symbols:
            raise Exception(
                f"Semantic Error (line {lineno}): Variable '{name}' not declared."
            )
        return self.symbols[name]

    def write_symbol_table(self, filename="symbol_table.txt"):
        """
        Write symbol table in a compiler-style format.
        """
        with open(filename, "w") as f:
            f.write(
                "Name\tType\tScope\tValue\tDeclaredAt\tLastUpdated\n"
            )
            f.write("-" * 70 + "\n")
            for name, info in self.symbols.items():
                f.write(
                    f"{name}\t{info['type']}\t{info['scope']}\t"
                    f"{info['value']}\t{info['declared_at']}\t"
                    f"{info['last_updated']}\n"
                )

# Optional test to demonstrate functionality
if __name__ == "__main__":
    analyzer = SemanticAnalyzer()
    try:
        analyzer.declare("x", "int", 1)       # Declare variable x of type int at line 1
        analyzer.declare("y", "float", 2)     # Declare variable y of type float at line 2
        analyzer.assign("x", 10, "int", 3)    # Assign value 10 to x at line 3
        analyzer.assign("y", 3.14, "float", 4) # Assign value 3.14 to y at line 4
        analyzer.lookup("x")                  # Check info of variable x
        analyzer.write_symbol_table()         # Save the symbol table to a file
        print("Semantic analysis completed successfully!")
    except Exception as e:
        print(e)