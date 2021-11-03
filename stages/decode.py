from Instruction import Instruction, InstructionFormat
import re

def decode(instruction, id):
    '''
    Retorna um dicionário contendo informações sobre a instrução

    Parâmetros:
        instruction (str): A instrução para ser decodificada
        id (int): Um número que identifica a instrução 
    '''

    # Parse da instrução
    splitted = list(filter(lambda s: s != "", re.split(r"[\s\t,()]", instruction)))
    name = splitted[0]

    # Formato e unidade funcional da instrução
    inst = _instructions.get(name)

    # Verifica se a instrução está implementada no nosso simulador
    if inst is None:
        print(f"AVISO: Instrução {name} não implementada ({id}:{instruction})")
        return None

    rd = -1
    rs1 = -1
    rs2 = -1
    imm = 0

    # Exemplo: lui	a0,0x1f
    if inst["format"] == InstructionFormat.RD_IMM or inst["format"] == InstructionFormat.RD_OFFSET:
        rd = _registers[splitted[1]]
        imm = int(splitted[2], base=16) if len(splitted) > 2 else 0

    # Exemplo: beq	a4,a3,10572
    elif inst["format"] == InstructionFormat.RS1_RS2_OFFSET:    
        rs1 = _registers[splitted[1]]
        rs2 = _registers[splitted[2]]
        imm = int(splitted[3])

    # Exemplo: lh	a3,12(s4)
    elif inst["format"] == InstructionFormat.RD_OFFSET_RS1:    
        rd = _registers[splitted[1]]
        imm = int(splitted[2])
        rs1 = _registers[splitted[3]]

    # Exemplo: lhu	a5,12(s4)
    elif inst["format"] == InstructionFormat.RS2_OFFSET_RS1:   
        rs2 =  _registers[splitted[1]]
        imm = int(splitted[2])
        rs1 = _registers[splitted[3]]

    # Exemplo: addi	sp,sp,-16
    elif inst["format"] == InstructionFormat.RD_RS1_IMM:
        rd = _registers[splitted[1]]
        rs1 = _registers[splitted[2]]
        imm = int(splitted[3])

    # Exemplo: slli	s7,s7,0x10
    elif inst["format"] == InstructionFormat.RD_RS1_SHAMT:    
        rd = _registers[splitted[1]]
        rs1 = _registers[splitted[2]]
        imm = int(splitted[3], base=16)

    # Exemplo: add	a3,a3,a4
    elif inst["format"] == InstructionFormat.RD_RS1_RS2:    
        rd = _registers[splitted[1]]
        rs1 = _registers[splitted[2]]
        rs2 = _registers[splitted[3]]

    return Instruction(name, id, rd, rs1, rs2, inst["uf"], imm, inst["format"])

_instructions = {
    "lui": {
        "format": InstructionFormat.RD_IMM,
        "uf": "load"
    },
    "auipc": {
        "format": InstructionFormat.RD_IMM,
        "uf": "add"
    },
    "jal": {
        "format": InstructionFormat.RD_OFFSET,
        "uf": "add"
    },
    "j": {
        "format": InstructionFormat.RD_OFFSET,
        "uf": "add"
    },
    "jalr": {
        "format": InstructionFormat.RD_OFFSET,
        "uf": "add"
    },
    "beq": {
        "format": InstructionFormat.RS1_RS2_OFFSET,
        "uf": "add"
    },
    "bne": {
        "format": InstructionFormat.RS1_RS2_OFFSET,
        "uf": "add"
    },
    "blt": {
        "format": InstructionFormat.RS1_RS2_OFFSET,
        "uf": "add"
    },
    "bge": {
        "format": InstructionFormat.RS1_RS2_OFFSET,
        "uf": "add" 
    },
    "bltu": {
        "format": InstructionFormat.RS1_RS2_OFFSET,
        "uf": "add" 
    },
    "bgeu": {
        "format": InstructionFormat.RS1_RS2_OFFSET,
        "uf": "add"
    },
    "lb": {
        "format": InstructionFormat.RD_OFFSET_RS1,
        "uf": "load"
    },
    "lh": {
        "format": InstructionFormat.RD_OFFSET_RS1,
        "uf": "load"
    },
    "lw": {
        "format": InstructionFormat.RD_OFFSET_RS1,
        "uf": "load" 
    },
    "lbu": {
        "format": InstructionFormat.RD_OFFSET_RS1,
        "uf": "load" 
    },
    "lhu": {
        "format": InstructionFormat.RS2_OFFSET_RS1,
        "uf": "load"
    },
    "sb": {
        "format": InstructionFormat.RS2_OFFSET_RS1,
        "uf": "load"
    },
    "sh": {
        "format": InstructionFormat.RS2_OFFSET_RS1,
        "uf": "load"
    },
    "sw": {
        "format": InstructionFormat.RS2_OFFSET_RS1,
        "uf": "load"
    },
    "addi": {
        "format": InstructionFormat.RD_RS1_IMM,
        "uf": "add"
    },
    "slti": {
        "format": InstructionFormat.RD_RS1_IMM,
        "uf": "add"
    },
    "sltiu": {
        "format": InstructionFormat.RD_RS1_IMM,
        "uf": "add"
    },
    "xori": {
        "format": InstructionFormat.RD_RS1_IMM,
        "uf": "add"
    },
    "ori": {
        "format": InstructionFormat.RD_RS1_IMM,
        "uf": "add"
    },
    "andi": {
        "format": InstructionFormat.RD_RS1_IMM,
        "uf": "add"
    },
    "slli": {
        "format": InstructionFormat.RD_RS1_SHAMT,
        "uf": "add"
    },
    "srli": {
        "format": InstructionFormat.RD_RS1_SHAMT,
        "uf": "add"
    },
    "srai": {
        "format": InstructionFormat.RD_RS1_SHAMT,
        "uf": "add"
    },
    "add": {
        "format": InstructionFormat.RD_RS1_RS2,
        "uf": "add"
    },
    "sub": {
        "format": InstructionFormat.RD_RS1_RS2,
        "uf": "add"
    },
    "sll": {
        "format": InstructionFormat.RD_RS1_RS2,
        "uf": "add"
    },
    "slt": {
        "format": InstructionFormat.RD_RS1_RS2,
        "uf": "add"
    },
    "sltu": {
        "format": InstructionFormat.RD_RS1_RS2,
        "uf": "add"
    },
    "xor": {
        "format": InstructionFormat.RD_RS1_RS2,
        "uf": "add"
    },
    "srl": {
        "format": InstructionFormat.RD_RS1_RS2,
        "uf": "add"
    },
    "sra": {
        "format": InstructionFormat.RD_RS1_RS2,
        "uf": "add"
    },
    "or": {
        "format": InstructionFormat.RD_RS1_RS2,
        "uf": "add"
    },
    "and": {
        "format": InstructionFormat.RD_RS1_RS2,
        "uf": "add"
    }
}

_registers = {
    "zero": 0,
    "x0": 0,
    "ra": 1,
    "sp": 2,
    "gp": 3,
    "tp": 4,
    "t0": 5,
    "t1": 6,
    "t2": 7,
    "s0": 8,
    "fp": 8,
    "s1": 9,
    "a0": 10,
    "a1": 11,
    "a2": 12,
    "a3": 13,
    "a4": 14,
    "a5": 15,
    "a6": 16,
    "a7": 17,
    "s2": 18,
    "s3": 19,
    "s4": 20,
    "s5": 21,
    "s6": 22,
    "s7": 23,
    "s8": 24,
    "s9": 25,
    "s10": 26,
    "s11": 27,
    "t3": 28,
    "t4": 29,
    "t5": 30,
    "t6": 31,
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "11": 11,
    "12": 12,
    "13": 13,
    "14": 14,
    "15": 15,
    "16": 16,
    "17": 17,
    "18": 18,
    "19": 19,
    "20": 20,
    "21": 21,
    "22": 22,
    "23": 23,
    "24": 24,
    "25": 25,
    "26": 26,
    "27": 27,
    "28": 28,
    "29": 29,
    "30": 30,
    "31": 31,
    "$0": 0,
    "$1": 1,
    "$2": 2,
    "$3": 3,
    "$4": 4,
    "$5": 5,
    "$6": 6,
    "$7": 7,
    "$8": 8,
    "$9": 9,
    "$10": 10,
    "$11": 11,
    "$12": 12,
    "$13": 13,
    "$14": 14,
    "$15": 15,
    "$16": 16,
    "$17": 17,
    "$18": 18,
    "$19": 19,
    "$20": 20,
    "$21": 21,
    "$22": 22,
    "$23": 23,
    "$24": 24,
    "$25": 25,
    "$26": 26,
    "$27": 27,
    "$28": 28,
    "$29": 29,
    "$30": 30,
    "$31": 31,
}