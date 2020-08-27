# 10000010 # LDI R0,10
# 00000000
# 00001010
# 10000010 # LDI R1,20
# 00000001
# 00010100
# 10000010 # LDI R2,TEST1
# 00000010
# 00010011
# 10100111 # CMP R0,R1
# 00000000
# 00000001
# 01010101 # JEQ R2
# 00000010
# 10000010 # LDI R3,1
# 00000011
# 00000001
# 01000111 # PRN R3
# 00000011
# # TEST1 (address 19):
# 10000010 # LDI R2,TEST2
# 00000010
# 00100000
# 10100111 # CMP R0,R1
# 00000000
# 00000001
# 01010110 # JNE R2
# 00000010
# 10000010 # LDI R3,2
# 00000011
# 00000010
# 01000111 # PRN R3
# 00000011
# # TEST2 (address 32):
# 10000010 # LDI R1,10
# 00000001
# 00001010
# 10000010 # LDI R2,TEST3
# 00000010
# 00110000
# 10100111 # CMP R0,R1
# 00000000
# 00000001
# 01010101 # JEQ R2
# 00000010
# 10000010 # LDI R3,3
# 00000011
# 00000011
# 01000111 # PRN R3
# 00000011
# # TEST3 (address 48):
# 10000010 # LDI R2,TEST4
# 00000010
# 00111101
# 10100111 # CMP R0,R1
# 00000000
# 00000001
# 01010110 # JNE R2
# 00000010
# 10000010 # LDI R3,4
# 00000011
# 00000100
# 01000111 # PRN R3
# 00000011
# # TEST4 (address 61):
# 10000010 # LDI R3,5
# 00000011
# 00000101
# 01000111 # PRN R3
# 00000011
# 10000010 # LDI R2,TEST5
# 00000010
# 01001001
# 01010100 # JMP R2
# 00000010
# 01000111 # PRN R3
# 00000011
# # TEST5 (address 73):
# 00000001 # HLT
import sys
HLT  = 1
LDI  = 130
PRN  = 71
MULT = 162
PUSH = 69
POP  = 70
CALL = 80
RET = 17
ADD = 160
JNE = 86
JMP = 84
JEQ = 85
CMP = 167
class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.pc = 0
        self.running = False
        self.reg = [None] * 9
        self.tos = 9

    def load(self, program):
        """Load a program into memory."""
        address = 0

        for instruction in program:
            self.ram[address] = int(instruction,2)
            address += 1
            
    def ram_write(self, operand_a,operand_b):
        self.reg[operand_a] = operand_b
            
    def ram_read(self):
        index = self.ram[self.pc + 1]
        print(self.reg[index])
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')


    def run(self):
        self.running = True
        while self.running:
            command = self.ram[self.pc]
            if command == HLT:
                self.running = False
                self.pc = 0
            elif command == PRN:
                self.ram_read()
                self.pc += 2
            elif command == LDI:
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                self.ram_write(operand_a, operand_b)
                self.pc += 3
            elif command == ADD:
                operand_a = self.reg[self.ram[self.pc + 1]]
                operand_b = self.reg[self.ram[self.pc + 2]]
                self.reg[self.ram[self.pc + 1]] += operand_b
                self.pc += 3
            elif command == MULT:
                operand_a = self.reg[self.ram[self.pc + 1]]
                operand_b = self.reg[self.ram[self.pc + 2]]
                self.reg[self.ram[self.pc+1]] = operand_a * operand_b
                self.reg[self.ram[self.pc+2]] = None
                self.pc += 3
            elif command == PUSH:
                self.tos -= 1
                self.reg[self.tos] = self.reg[self.ram[self.pc + 1]]
                self.pc += 2
            elif command == POP:            
                popped_value = self.reg[self.tos]
                register_number = self.ram[self.pc + 1]
                self.reg[register_number] = popped_value
                self.tos += 1
                self.pc += 2
            elif command == CALL:
                next_inst = self.pc + 2
                self.tos -= 1
                self.reg[self.tos] = next_inst
                reg_address = self.ram[self.pc + 1]
                address_to_jump_to = self.reg[reg_address]
                self.pc = address_to_jump_to
                print(self.reg)
            elif command == RET:
                return_address = self.reg[self.tos]
                self.tos += 1
                self.pc = return_address
            elif command == CMP:
                operand_a = self.reg[self.ram[self.pc + 1]]
                operand_b = self.reg[self.ram[self.pc + 2]]
                jump = self.ram[self.pc+3]
                if jump == JEQ and operand_a == operand_b:
                    self.pc = self.reg[self.ram[self.pc+4]]
                elif jump == JNE and operand_a != operand_b:
                    self.pc = self.reg[self.ram[self.pc+4]]
                else:
                    self.pc += 5
            elif command == JMP:
                 self.pc = self.reg[self.ram[self.pc+1]]
            else:
                self.pc += 1