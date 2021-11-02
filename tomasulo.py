import pandas as pd
import json
import numpy as np
import sys
from decode import decode
from emission import emission
from execution import execution
from write import write

def main():
    
    config = load_config()

    if len(sys.argv) < 2:
        print("Usage: python tomasulo.py <file>")
        return 1

    assembly_path = sys.argv[1]
    instructions = get_instructions_from(assembly_path)
    registers, rs, mem, inst_queue, times, fu = initialize_tables(config, instructions)
    clock = 0
    instruction = None
    instruction_id = 0

    # Enquanto existirem instruções para executar e se as reservation stations não estiverem vazias
    while len(instructions) != 0 or len(rs[rs["busy"] == True]) != 0:        

        # Caso um instrução foi emitida no ciclo anterior
        if instruction is None and len(instructions) > 0:
            instruction = instructions.pop(0)
            instruction = decode(instruction, instruction_id)
            if instruction is not None:
                instruction.add_time(clock)
                instruction_id += 1

        if emission(rs, registers, config, instruction, clock, times):
            instruction = None

        rs_completed = execution(rs, registers, config, clock, times, mem, fu)
        if rs_completed:
            write(rs, registers, config, clock, times, mem, fu, rs_completed)

        clock += 1

    
    

def initialize_tables(config, instructions):
    # Cria tabela para os registradores
    registers = pd.DataFrame({
        "q_i": ["" for _ in range(config["registers"])],
        "value": [0 for _ in range(config["registers"])]
    }, 
    index=[f"r{i}" for i in range(config["registers"])])

    # Cria tabelas as reservations stations
    rs_count = sum((config["reservation-stations"][fu] for fu in config["reservation-stations"]))
    rs = pd.DataFrame({
        "time": [0 for _ in range(rs_count)],
        "busy": [False for _ in range(rs_count)],
        "op": ["" for _ in range(rs_count)],
        "v_j": [0 for _ in range(rs_count)],
        "v_k": [0 for _ in range(rs_count)],
        "q_j": ["" for _ in range(rs_count)],
        "q_k": ["" for _ in range(rs_count)],
        "addr": [0 for _ in range(rs_count)],
        "instruction_id": [0 for _ in range(rs_count)]
        },
        index=[f"{fu}{i}" for fu in config["reservation-stations"] for i in range(config["reservation-stations"][fu])]
    )

    for col in rs.columns:
        rs[col].values[:] = 0

    # Cria array para memória
    mem = np.zeros(config["mem_size"], dtype=np.int32)

    # Cria instruction queue
    inst_queue = pd.Series(np.array(config["instruction_queue_size"], dtype=object)) 

    # Cria tabela de tempos para as instruções
    program_size = len(instructions)
    times = pd.DataFrame({
        "instruction": instructions,
        "emission": [0 for _ in range(program_size)],
        "exec_start": [0 for _ in range(program_size)],
        "exec_end": [0 for _ in range(program_size)],
        "write": [0 for _ in range(program_size)]
        }
    )

    # Cria tabela de usos das unidades funcionais
    fu_index = [f"{fu}{i}" for fu in config["fu"] for i in range(config["fu"][fu])]
    fu = pd.DataFrame({
        "busy": [False for _ in range(len(fu_index))],
        "reservation_station": ["" for _ in range(len(fu_index))]
        },
        index=fu_index
    )

    return registers, rs, mem, inst_queue, times, fu

def get_instructions_from(file_path):
    with open(file_path, "r") as f:
        return [line.rstrip() for line in f]

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

main()