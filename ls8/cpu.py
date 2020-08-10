"""CPU functionality."""
# 10000010 # LDI R0,8
# 00000000
# 00001000
# 10000010 # LDI R1,9
# 00000001
# 00001001
# 10100010 # MUL R0,R1
# 00000000
# 00000001
# 01000111 # PRN R0
# 00000000
# 00000001 # HLT

import sys
HLT =  1
LDI =  130
PRN =  71
MULT = 162

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.pc = 0
        self.running = False
        self.reg = [None] * 6

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
                         
