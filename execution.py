def execution(reservation_stations, registers, config, cur_cycle, times, mem, fu):
    '''
    Realiza a emissão da instrução. (Atualiza a tabela "times"; atualiza o tempo das instruções executando na tabela "reservation_stations"; para cada nova instrução executando atualiza a tabela "fu" para indicar que a unidade funcional está ocupada)
    Retorna qual reservation station terminou a execução neste ciclo, caso nenhuma instrução tenha terminado execução neste ciclo retornar None

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

        fu (pandas.DataFrame): tabela com estado atual das unidades funcionais. Use essa tabela para verificar se 
        as unidades funcionais estão livres e para determinar quais instruções estão executando para reduzir o tempo de execução nas reservation stations.
        Exemplo:

                    busy reservation_station
            load0   True               load0
            add0   False                    
            mult0  False                     
    '''

    ##########################
    ### Implementação aqui ###
    ##########################

    # return reservation station
   