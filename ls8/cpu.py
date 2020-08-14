  
# 10000010 # LDI R1,MULT2PRINT
# 00000001
# 00011000
# 10000010 # LDI R0,10
# 00000000
# 00001010
# 01010000 # CALL R1
# 00000001
# 10000010 # LDI R0,15
# 00000000
# 00001111
# 01010000 # CALL R1
# 00000001
# 10000010 # LDI R0,18
# 00000000
# 00010010
# 01010000 # CALL R1
# 00000001
# 10000010 # LDI R0,30
# 00000000
# 00011110
# 01010000 # CALL R1
# 00000001
# 00000001 # HLT
# # MULT2PRINT (address 24):
# 10100000 # ADD R0,R0
# 00000000
# 00000000
# 01000111 # PRN R0
# 00000000
# 00010001 # RET
import sys
HLT  = 1
LDI  = 130
PRN  = 71
MULT = 162
PUSH = 69
POP  = 70
CALL = 80
RET = 17

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
            if command == PRN:
                
                self.ram_read()
                self.pc += 2
            if command == LDI:
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                self.ram_write(operand_a, operand_b)
                self.pc += 3
            if command == MULT:
                operand_a = self.reg[self.ram[self.pc + 1]]
                operand_b = self.reg[self.ram[self.pc + 2]]
                self.reg[self.ram[self.pc+1]] = operand_a * operand_b
                self.reg[self.ram[self.pc+2]] = None
                self.pc += 3    
            if command == PUSH:
                self.tos -= 1
                self.reg[self.tos] = self.reg[self.ram[self.pc + 1]]
                self.pc += 2
            if command == POP:            
                popped_value = self.reg[self.tos]
                register_number = self.ram[self.pc + 1]
                self.reg[register_number] = popped_value
                self.tos += 1
                self.pc += 2
            if command == CALL:
                next_inst = pc + 2
                self.tos -= 1
                self.ram[self.tos] = next_inst
                reg_address = self.ram[self.pc + 1]
                address_to_jump_to = self.reg[reg_address]
                self.pc = address_to_jump_to
            if command == RET:
                return_address = self.ram[self.tos]
                self.tos += 1
                self.pc = return_address
