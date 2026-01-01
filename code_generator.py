class CodeGenerator:
    def __init__(self):
        self.ir = []
        self.py_code = []

    def generate_expression(self, temp, op1, operator, op2):
        self.ir.append(f"{temp} = {op1} {operator} {op2}")

    def generate_assignment(self, lhs, rhs):
        self.ir.append(f"{lhs} = {rhs}")

    def write_output(self):
        with open("ir.txt", "w") as f:
            for line in self.ir:
                f.write(line + "\n")