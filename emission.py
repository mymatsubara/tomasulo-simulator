def emission(reservation_stations, registers, config, instruction, cur_cycle, times):
    '''
    Realiza a emissão da instrução (atualiza a reservation station para ter as informações da instrução emitida; atualiza a tabela "times")
    Retorna True se a instrução foi emitida, caso contrário False

    Parâmetros:
        reservation_stations (pandas.DataFrame): tabela das reservation stations a ser atualizada. Exemplo:
                    time   busy op  v_j  v_k q_j q_k  addr  instruction_id
            load0      0  False  0    0    0   0   0     0               0
            adder0     0  False  0    0    0   0   0     0               0
            adder1     0  False  0    0    0   0   0     0               0
            mult0      0  False  0    0    0   0   0     0               0

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

    ##########################
    ### Implementação aqui ###
    ##########################

    # return True or False
   