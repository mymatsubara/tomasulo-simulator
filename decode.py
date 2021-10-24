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

    splitted = instruction.split(" ")
    name = splitted[0]
    # Exemplo de implementação do add (talvez tenha que alterar)
    if (name == "add"):
        # add 1, 2, 3
        splitted = [s.strip(",") for s in splitted]
        return Instruction(name, id, int(splitted[1]), int(splitted[2]), int(splitted[3]), "add")


    # Tudo que está entre [chaves] é para ser substituído
    # return Instruction("[name: string]", id, [rd: int], [rs1: int], [rs2: int], [uf: "load"|"add"|"mult"])
    # return Instruction("lb", id, 1, 2, -1, "load")
    # load 