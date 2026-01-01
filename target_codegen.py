class TargetCodeGenerator:
    def __init__(self, ir_file, target_file):
        self.ir_file = ir_file
        self.target_file = target_file
        self.registers = {}
        self.reg_count = 0
        self.target_code = []

    def new_register(self):
        self.reg_count += 1
        return f"R{self.reg_count}"

    def get_register(self, var):
        if var not in self.registers:
            self.registers[var] = self.new_register()
        return self.registers[var]

    def generate(self):
        with open(self.ir_file, "r") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or "=" not in line:
                continue

            lhs, rhs = map(str.strip, line.split("="))

            lhs_reg = self.get_register(lhs)

            # Constant assignment
            if rhs.isdigit():
                self.target_code.append(f"LOAD {lhs_reg}, {rhs}")

            # Variable assignment
            else:
                rhs_reg = self.get_register(rhs)
                self.target_code.append(f"MOV {lhs_reg}, {rhs_reg}")

    def write_target_code(self):
        with open(self.target_file, "w") as f:
            for instr in self.target_code:
                f.write(instr + "\n")
