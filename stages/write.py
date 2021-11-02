def write(reservation_stations, registers, config, cur_cycle, times, mem, fu, reservation_station_completed):
    '''
    Escreve os resultados (atualiza a "mem" de acordo com a instrução concluída; atualiza a tabela "times"; para a instrução concluída atualiza a tabela "fu" para indicar que a unidade funcional está livre; remove a instrução da reservation station; escreve os resultados da instrução nos registradores)

    Parâmetros:
        reservation_stations (pandas.DataFrame): tabela das reservation stations a ser atualizada. Exemplo:
                    time   busy op  v_j  v_k q_j q_k  addr  instruction
            load0      0  False  0    0    0   0   0     0         None
            adder0     0  False  0    0    0   0   0     0         None      
            adder1     0  False  0    0    0   0   0     0         None      
            mult0      0  False  0    0    0   0   0     0         None      

        registers: (pandas.DataFrame): tabela dos registradores a ser atualizada. Exemplo:
                q_i  value
            r0           0
            r1           0
            r2           0

        config (dict): dicionário com as configurações do simulador. O arquivo config.json contém os campos do dicionário.        

        cur_cycle (int): ciclo atual da simulação

        times (pandas.DataFrame): tabela dos tempos das instruções para ser atualizada. Use o instruction_id para encontrar a instrução em questão na tabela. Exemplo:
               instruction  emission  exec_start  exec_end  write
            0  add 1, 2, 3         0           0         0      0
            1  add 1, 2, 3         0           0         0      0
            2  add 1, 2, 3         0           0         0      0
            3  add 1, 2, 3         0           0         0      0

        mem (numpy.narray): array que representa a memória do computador simulado.

        fu (pandas.DataFrame): tabela com estado atual das unidades funcionais.
        Atualize o estado da unidade funcional caso a instrução correspondente escreva o resultado.
        Exemplo:

                    busy reservation_station
            load0   True               load0
            add0   False                    
            mult0  False 

        reservation_station_completed (str): nome da reservation station cuja instrução foi concluída
    '''
    
    # Dados sobre a instrução que vai ser escrita
    rs = reservation_stations.loc[reservation_station_completed]
    instruction = rs.instruction

    # Como a função write só executa quando uma instrução termina, não é necessário verificar o termino da instrução em questão. Além disso,
    # como apenas uma instrução entra nesta função por ciclo, também não será necessário verificar se o CDB está livre.
    if instruction.is_store() and rs.q_k == 0:
        mem[rs.addr] = rs.v_k
    else:
        # Atualiza o valor Qi dos registradores
        registers[registers["q_i"] == reservation_station_completed] = ["", rs.v_k]

        # Atualiza o valor Qj das reservation stations
        reservation_stations.loc[reservation_stations["q_j"] == reservation_station_completed, ["q_j", "v_j"]] = [0, rs.v_k]

        # Atualiza o valor Qk das reservation stations
        reservation_stations.loc[reservation_stations["q_k"] == reservation_station_completed, ["q_k", "v_k"]] = [0, rs.v_k]


    # Marca a unidade funcional utilizada como livre
    fu[fu["reservation_station"] == reservation_station_completed] = [False, ""]

    # Atualiza a tabela de tempos para as instruções
    times.loc[instruction.id, "write"] = cur_cycle + 1

    # Limpa a reservation station
    reservation_stations.loc[reservation_station_completed] = [0, False, 0, 0, 0, 0, 0, 0, 0]