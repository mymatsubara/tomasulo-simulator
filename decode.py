from Instruction import Instruction

def decode(instruction, id):
    '''
    Retorna um dicionário contendo informações sobre a instrução

    Parâmetros:
        instruction (str): A instrução para ser decodificada
        id (int): Um número que identifica a instrução 
    '''
    ##########################
    ### Implementação aqui ###
    ##########################

    # Tudo que está entre [chaves] é para ser substituído
    # return Instruction([name: string], id, [rd: int], [rs1: int], [rs2: int], [uf: "load"|"add"|"mult"])