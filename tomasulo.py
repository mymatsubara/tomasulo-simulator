import pandas as pd
import json
import numpy as np
import sys
from stages.decode import decode
from stages.emission import emission
from stages.execution import execution
from stages.write import write
import warnings
warnings.filterwarnings('ignore')

def main():
    
    config = load_config()

    if len(sys.argv) < 2:
        print("Usage: python tomasulo.py <file>")
        return 1

    assembly_path = sys.argv[1]
    instructions = get_instructions_from(assembly_path)
    registers, rs, mem, times, fu = initialize_tables(config, instructions)
    clock = 0
    instruction = None
    instruction_id = 0

    print("INSTRUÇÕES:")
    print(f"- " + '\n- '.join(instructions) + "\n")


    print("!!!!!!!!!!!!!!! INÍCIO DA SIMULAÇÃO !!!!!!!!!!!!!!!\n")

    # Enquanto existirem instruções para executar e se as reservation stations não estiverem vazias
    while len(instructions) != 0 or len(rs[rs["busy"] == True]) != 0:
        print(f"\n================== CICLO: {clock+1}==================")        

        # Caso um instrução foi emitida no ciclo anterior
        if instruction is None and len(instructions) > 0:
            instruction = instructions.pop(0)
            instruction = decode(instruction, instruction_id)
            if instruction is not None:                
                instruction_id += 1

        if emission(rs, registers, config, instruction, clock, times):
            instruction = None

        rs_completed = execution(rs, registers, config, clock, times, mem, fu)

        if rs_completed:
            write(rs, registers, config, clock, times, mem, fu, rs_completed)

        print("INSTRUÇÃO EMITIDA\nRESERVATION STATIONS:")
        print(rs.loc[:, rs.columns != "instruction"])
        print("\nREGISTRADORES:")
        print(registers)
        print("\nUNIDADES FUNCIONAIS:")
        print(fu)

        clock += 1

    print(f"!!!!!!!!!!!!!!! FIM DA SIMULAÇÃO (CICLOS: {clock+1}) !!!!!!!!!!!!!!!\n")
    print(f"TABELA DE TEMPOS:")
    print(times)
    

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
        "instruction": [None for _ in range(rs_count)]
        },
        index=[f"{fu}{i}" for fu in config["reservation-stations"] for i in range(config["reservation-stations"][fu])]
    )

    for col in rs.columns:
        rs[col].values[:] = 0

    # Cria array para memória
    mem = np.zeros(config["mem_size"], dtype=np.int32)

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

    return registers, rs, mem, times, fu

def get_instructions_from(file_path):
    with open(file_path, "r") as f:
        return [line.rstrip() for line in f]

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

main()