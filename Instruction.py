from enum import Enum

class InstructionFormat(Enum):
    RD_IMM = 0,
    RD_OFFSET = 1,
    RS1_RS2_OFFSET = 2,
    RD_OFFSET_RS1 = 3,
    RS2_OFFSET_RS1 = 4,
    RD_RS1_IMM = 5, 
    RD_RS1_SHAMT = 6,
    RD_RS1_RS2 = 7

class Instruction:
    def __init__(self, name, id, rd, rs1, rs2, uf, imm, i_format):
        self.name = name
        self.id = id
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.uf = uf
        self.imm = imm
        self.i_format = i_format

    def add_time(self, time):
        self.time = time
