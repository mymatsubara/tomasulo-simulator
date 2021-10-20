class Instruction:
    def __init__(self, name, id, rd, rs1, rs2, uf):
        self.name = name
        self.id = id
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.uf = uf

    def add_time(self, time):
        self.time = time
