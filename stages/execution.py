import numpy as np

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
    bus_user = ""

    # ====== ADD ========

    # Reservation stations add
    rs_add_mask  = reservation_stations.index.str.contains("add.*")
    rs_add = reservation_stations[rs_add_mask]

    # Lista de unidades funcionais add
    add_fu_mask = fu.index.str.contains("add.*")
    add_fu = fu.loc[add_fu_mask]
    busy_add_fu = add_fu[add_fu["busy"] == True]

    # Reduzir o tempo das intruções que estão executando
    reservation_stations.loc[busy_add_fu["reservation_station"], "time"] = np.max(reservation_stations.loc[busy_add_fu["reservation_station"], "time"]-1, 0)

    # Lista de reservation stations com instruções concluídas
    rs_add_mask  = reservation_stations.index.str.contains("add.*")
    rs_add = reservation_stations[rs_add_mask]
    completed_adds = rs_add[(rs_add["time"] == 0) & (rs_add["busy"] == True)]

    if len(completed_adds) > 0:
        # Prioridade do bus para instruções com id menor
        completed_adds["id"] = list(map(lambda i: i.id, completed_adds.instruction))
        completed_adds = completed_adds.sort_values(by=["id"])
        bus_user = completed_adds.index[0]

        instruction = completed_adds.iloc[0]["instruction"]
        op = _op.get(instruction)
        if op:
            reservation_stations.loc[completed_adds.iloc[0], "v_k"] = op(executing_rs_ld.v_j, executing_rs_ld.v_k, mem, executing_rs_ld.addr)

        # Atualiza o tempo de fim de execução da instrução
        times.loc[instruction.id, "exec_end"] = cur_cycle + 1


    # Lista das reservation station add com instruções que ainda não começaram a executar
    
    ready_rs_add = rs_add[(rs_add["busy"] == True) & (list(map(lambda i: i not in busy_add_fu["reservation_station"], rs_add.index)))]

    # Se houver uf livre
    free_fu = add_fu[add_fu["busy"] == False]
    if len(free_fu) > 0 and len(ready_rs_add) > 0:
        # Escolhe qual instrução irá executar com base no id
        ready_rs_add["id"] = list(map(lambda i: i.id, ready_rs_add.instruction))
        ready_rs_add = ready_rs_add.sort_values(by=["id"])
        exec_rs_add = ready_rs_add.iloc[0]

        # Unidade funcional marcada como ocupada
        fu.loc[free_fu.index[0]] = [True, ready_rs_add.index[0]]

        # Atualiza a tabela de tempos
        times.loc[exec_rs_add["id"], "exec_start"] = cur_cycle + 2


    # ====== MULT ========

    # Reservation stations add
    rs_mult_mask  = reservation_stations.index.str.contains("mult.*")
    rs_mult = reservation_stations[rs_mult_mask]

    # Lista de unidades funcionais mult
    mult_fu_mask = fu.index.str.contains("mult.*")
    mult_fu = fu.loc[mult_fu_mask]
    busy_mult_fu = mult_fu[mult_fu["busy"] == True]

    # Reduzir o tempo das intruções que estão executando
    reservation_stations.loc[busy_mult_fu["reservation_station"], "time"] = np.max(reservation_stations.loc[busy_mult_fu["reservation_station"], "time"]-1, 0)

    # Lista de reservation stations com instruções concluídas
    rs_mult_mask  = reservation_stations.index.str.contains("mult.*")
    rs_mult = reservation_stations[rs_mult_mask]
    completed_mults = rs_mult[(rs_mult["time"] == 0) & (rs_mult["busy"] == True)]

    if len(completed_mults) > 0 and not bus_user:
        # Prioridade do bus para instruções com id menor
        completed_mults["id"] = list(map(lambda i: i.id, completed_mults.instruction))
        completed_mults = completed_mults.sort_values(by=["id"])
        bus_user = completed_mults.index[0]

        instruction = completed_mults.iloc[0]["instruction"]
        op = _op.get(instruction)
        if op:
            reservation_stations.loc[completed_mults.iloc[0], "v_k"] = op(executing_rs_ld.v_j, executing_rs_ld.v_k, mem, executing_rs_ld.multr)

        # Atualiza o tempo de fim de execução da instrução
        times.loc[instruction.id, "exec_end"] = cur_cycle + 1


    # Lista das reservation station mult com instruções que ainda não começaram a executar
    
    ready_rs_mult = rs_mult[(rs_mult["busy"] == True) & (list(map(lambda i: i not in busy_mult_fu["reservation_station"], rs_mult.index)))]

    # Se houver uf livre
    free_fu = mult_fu[mult_fu["busy"] == False]
    if len(free_fu) > 0 and len(ready_rs_mult) > 0:
        # Escolhe qual instrução irá executar com base no id
        ready_rs_mult["id"] = list(map(lambda i: i.id, ready_rs_mult.instruction))
        ready_rs_mult = ready_rs_mult.sort_values(by=["id"])
        exec_rs_mult = ready_rs_mult.iloc[0]

        # Unidade funcional marcada como ocupada
        fu.loc[free_fu.index[0]] = [True, ready_rs_mult.index[0]]

        # Atualiza a tabela de tempos
        times.loc[exec_rs_mult["id"], "exec_start"] = cur_cycle + 2


    # ====== LD ======= 
    

    # Reservation stations load/stores prontas para executar
    rs_ld_mask = reservation_stations.index.str.contains("load.*")
    rs_ld = reservation_stations[rs_ld_mask]
    ready_rs_ld = rs_ld[(rs_ld["q_j"] == 0) & (rs_ld["busy"] == True)]

    # Se existe alguma reservation station pronta para executar
    if len(ready_rs_ld) > 0:
        # Ordena load/stores por ordem de chegada
        ready_rs_ld["sort"] = list(map(lambda i: i.id if i else np.inf, ready_rs_ld.instruction.values))
        ready_rs_ld = ready_rs_ld.sort_values(by=["sort"])
        executing_rs_ld = ready_rs_ld.iloc[0]
        instruction = executing_rs_ld.instruction

        # Se início de execução da instrução
        if executing_rs_ld["time"] == instruction.time:
            times.loc[instruction.id, "exec_start"] = cur_cycle + 2
            reservation_stations.loc[ready_rs_ld.index[0], "addr"] += reservation_stations.loc[ready_rs_ld.index[0], "v_k"]
            reservation_stations.loc[ready_rs_ld.index[0], "time"] -= 1   
            
        # Se a instrução terminou de executar
        elif reservation_stations.loc[ready_rs_ld.index[0], "time"] == 0:
            if not bus_user:
                bus_user = ready_rs_ld.index[0]
                op = _op.get(instruction.name)
                if op:
                    reservation_stations.loc[ready_rs_ld.index[0], "v_k"] = op(executing_rs_ld.v_j, executing_rs_ld.v_k, mem, executing_rs_ld.addr)
                times.loc[instruction.id, "exec_end"] = cur_cycle + 1

        # Se a instrução está executando
        elif times.loc[instruction.id, "exec_start"] <= cur_cycle:
            reservation_stations.loc[ready_rs_ld.index[0], "time"] -= 1                
        
    return bus_user


def sb(v_j, v_k, mem, addr):
    mem[addr] = v_k & 0xff
    return 0   
def sh(v_j, v_k, mem, addr):
    mem[addr] = v_k & 0xffff
    return 0
def sw(v_j, v_k, mem, addr):
    mem[addr] = v_k
    return 0
def lb(v_j, v_k, mem, addr):
    return mem[addr] & 0xff
def lh(v_j, v_k, mem, addr):
    return mem[addr] & 0xffff
def lw(v_j, v_k, mem, addr):
    return mem[addr]
def lbu(v_j, v_k, mem, addr):
    return mem[addr] & 0xff000000
def lhu(v_j, v_k, mem, addr):
    return mem[addr]& 0xffff0000

_op = {
    "add": lambda v_j, v_k, mem, addr: v_j + v_k, # x[rd] = x[rs1] + x[rs2]
    "addi": lambda v_j, v_k, mem, addr: v_j + v_k, # x[rd] = x[rs1] + sext(immediate)
    "sub": lambda v_j, v_k, mem, addr: v_j - v_k,

    "sb": sb, 
    "sh": sh, 
    "sw": sw, # M[x[rs1] + sext(offset)] = x[rs2][31:0]
    #mem[addr] = v_k
    
    "lb": lb, # adicionar sign extend        
    "lh": lh,
    "lw": lw,
    "lbu": lbu, # adicionar zero extend        
    "lhu": lhu, 
    "and": lambda v_j, v_k, mem, addr: v_j & v_k,
    "andi": lambda v_j, v_k, mem, addr: v_j & v_k,
    "ori": lambda v_j, v_k, mem, addr: v_j | v_k,
    "or": lambda v_j, v_k, mem, addr: v_j | v_k,
    "xori": lambda v_j, v_k, mem, addr: v_j ^ v_k,
    "xor": lambda v_j, v_k, mem, addr: v_j ^ v_k,

    "slli": lambda v_j, v_k, mem, addr: v_j << v_k[-5:],
    "srli": lambda v_j, v_k, mem, addr: v_j >> v_k[-5:],
    "sll": lambda v_j, v_k, mem, addr: v_j << v_k[-5:],
    "srl": lambda v_j, v_k, mem, addr: v_j >> v_k[-5:],

    "lui": lambda v_j, v_k, mem, addr: v_k << 12,
}