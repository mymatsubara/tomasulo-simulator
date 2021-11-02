def emission(reservation_stations, registers, config, instruction, cur_cycle, times):
    '''
    Realiza a emissão da instrução (atualiza a reservation station para ter as informações da instrução emitida; atualiza a tabela "times")
    Retorna True se a instrução foi emitida, caso contrário False

    Parâmetros:
        reservation_stations (pandas.DataFrame): tabela das reservation stations a ser atualizada. Exemplo:
                    time   busy op  v_j  v_k q_j q_k  addr  instruction
            load0      0  False  0    0    0   0   0     0          None
            adder0     0  False  0    0    0   0   0     0          None
            adder1     0  False  0    0    0   0   0     0          None
            mult0      0  False  0    0    0   0   0     0          None

        registers: (pandas.DataFrame): tabela dos registradores a ser atualizada. Exemplo:
                q_i  value
            r0           0
            r1           0
            r2           0

        config (dict): dicionário com as configurações do simulador. O arquivo config.json contém os campos do dicionário.

        instruction (Instruction): objeto com as informações da instrução emitida. O arquivo Instruction.py contém a declaração da classe Instruction.

        cur_cycle (int): ciclo atual da simulação

        times (pandas.DataFrame): tabela dos tempos das instruções para ser atualizada. Use o instruction.id para encontrar a instrução em questão na tabela. Exemplo:
               instruction  emission  exec_start  exec_end  write
            0  add 1, 2, 3         0           0         0      0
            1  add 1, 2, 3         0           0         0      0
            2  add 1, 2, 3         0           0         0      0
            3  add 1, 2, 3         0           0         0      0

    '''
    print("++++++++++++++++ EMISSÃO ++++++++++++++++\n")

    if instruction is None:
        print("Não há mais instruções na fila para emitir.")
        return False

    print(f"Tentando emitir instrução: {times.loc[instruction.id, 'instruction']} (uf: {instruction.uf})")

    uf = instruction.uf

    if uf not in ["load", "add", "mult"]:
        raise Exception(f"Unidade funcional invalida: {uf} - instrução {instruction.name}")

    # Descobrindo quais reservation stations estão livres para a instrução a ser emitida
    free_rs = reservation_stations[reservation_stations["busy"] == False]
    free_rs_index = free_rs.index.str.contains(uf+".*")
    free_rs = free_rs.index[free_rs_index]
    if len(free_rs) == 0:
        print(f"NENHUMA INSTRUÇÃO EMITIDA.\nTodas as reservation stations para unidades funcionais {uf} estão cheias!")
        return False
    
    # Nome da reservation station livre na qual será alocada a instrução
    free_rs_name = free_rs[0]

    # Preenche colunas op, busy e time
    reservation_stations.loc[free_rs_name, "op"] = instruction.name
    reservation_stations.loc[free_rs_name, "busy"] = True
    reservation_stations.loc[free_rs_name, "time"] = config["instructions_time"][instruction.name]

    # Se a instrução possui operando rs1
    if instruction.rs1 >= 0:
        rs = f"r{instruction.rs1}"

        # Se o registrador rs tem resultado pendente
        if registers.loc[rs, 'q_i']:
            reservation_stations.loc[free_rs_name, 'q_j'] = registers.loc[rs, 'q_i']            
        else:
            # Atualiza os valores de Vj, Qj e addr
            reservation_stations.loc[free_rs_name, 'v_j'] = registers.loc[rs, 'value']
            reservation_stations.loc[free_rs_name, 'q_j'] = 0
            if (uf == 'load'):
                reservation_stations.loc[free_rs_name, 'addr'] = instruction.imm

    # Se a instrução possui operando rs2
    if instruction.rs2 >= 0:       
        rt = f"r{instruction.rs2}"

        # Se o registrador rt tem resultado pendente
        if registers.loc[rt, 'q_i']:
            reservation_stations.loc[free_rs_name, 'q_k'] = registers.loc[rt, 'q_i'] 
        else:
            # Atualiza os valores de Vk, Qk e addr
            reservation_stations.loc[free_rs_name, 'v_k'] = registers.loc[rt, 'value'] 
            reservation_stations.loc[free_rs_name, 'q_k'] = 0
    
    # Se a instrução possui registrador de destino
    if instruction.rd >= 0:
        rd = f"r{instruction.rd}"
        registers.loc[rd, "q_i"] = free_rs_name
        
    # Atualiza tabela de tempos das instruções
    times.loc[instruction.id, "emission"] = cur_cycle + 1

    print("INSTRUÇÃO EMITIDA\nRESERVATION STATIONS:")
    print(reservation_stations)
    print("\nREGISTRADORES:")
    print(registers)

    return True