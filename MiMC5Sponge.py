import json


class MiMC5Sponge:
    def __init__(self):
        self.nRounds = 20
        self.p = 21888242871839275222246405745257275088548364400416034343698204186575808495617
        with open('files/c_values.json') as fp:
            self.c_values = json.load(fp)
    
    def __feistel(self, inL, inR, k):
        lastL, lastR = inL, inR
        
        for i in range(self.nRounds):
            mask = (lastR + k + self.c_values[i]) % self.p
            mask5 = pow(mask, 5, self.p)
            
            lastL, lastR = lastR, (lastL + mask5) % self.p
        
        return lastL, lastR


m = MiMC5Sponge()