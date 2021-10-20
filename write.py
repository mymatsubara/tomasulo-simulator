def write(reservation_stations, registers, config, cur_cycle, times, mem, fu, reservation_station_completed):
        '''
    Escreve os resultados (atualiza a "mem" de acordo com a instrução concluída; atualiza a tabela "times"; para a instrução concluída atualiza a tabela "fu" para indicar que a unidade funcional está livre; remove a instrução da reservation station; escreve os resultados da instrução nos registradores)

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

    ##########################
    ### Implementação aqui ###
    ##########################