"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.sp = 7
        self.fl = 0b00000000

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2)
                # print(v)
                self.ram[address] = v
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        ADD = 0b10100000
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        halted = False

        while not halted:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == LDI:
                # Set the value of a register to an integer
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif instruction == PRN:
                # Print numeric value stored in the given register.
                # Print to the console the decimal integer value that is stored in the given register.
                print(self.reg[operand_a])
                self.pc += 2
            elif instruction == ADD:
                self.reg[operand_a] += self.reg[operand_b]
                self.pc += 3
            elif instruction == MUL:
                # Multiply the values in two registers together and store the result in registerA.
                result = self.reg[operand_a] * self.reg[operand_b]
                print(result)
                self.pc += 3
            elif instruction == PUSH:
                # Get register number
                # Get value out of the register
                val = self.reg[operand_a]
                # Decrement the SP
                self.reg[self.sp] -= 1
                # Store value in memory at SP
                self.ram[self.reg[self.sp]] = val
                self.pc += 2
            elif instruction == POP:
                # Get register number
                # Get value out of the register
                val = self.ram[self.reg[self.sp]]
                # Store value in memory at SP
                self.reg[operand_a] = val
                # Increment the SP
                self.reg[self.sp] += 1
                self.pc += 2
            elif instruction == CALL:
                return_addr = self.pc + 2
                # Push it on the stack
                self.reg[self.sp] -= 1
                top_of_stack_addr = self.reg[self.sp]
                self.ram[top_of_stack_addr] = return_addr
                # Set the PC to the subroutine addr
                subroutine_addr = self.reg[operand_a]
                self.pc = subroutine_addr
            elif instruction == RET:
                # Pop the return addr off stack
                top_of_stack_addr = self.reg[self.sp]
                return_addr = self.ram[top_of_stack_addr]
                self.reg[self.sp] += 1
                # Store it in the PC
                self.pc = return_addr
            elif instruction == CMP:
                if self.reg[operand_a] == self.reg[operand_b]:
                    self.fl = 1
                else:
                    self.fl = 0
                self.pc += 3
            elif instruction == JMP:
                self.pc = self.reg[operand_a]
            elif instruction == JEQ:
                if self.fl == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif instruction == JNE:
                if self.fl == 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif instruction == HLT:
                # Halt the CPU (and exit the emulator).
                halted = True
            else:
                print(
                    f'Unknown instruction {instruction} at address {self.pc}.')
                sys.exit()
