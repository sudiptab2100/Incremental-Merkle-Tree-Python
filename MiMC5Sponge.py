import json


class MiMC5Sponge:
    def __init__(self):
        self.p = 21888242871839275222246405745257275088548364400416034343698204186575808495617
        with open('files/c_values.json') as fp:
            self.c_values = json.load(fp)


m = MiMC5Sponge()