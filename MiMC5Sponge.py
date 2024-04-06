import json


class MiMC5Sponge:
    def __init__(self):
        with open('files/MiMC_settings.json') as fp:
            micmcSettings = json.load(fp)
        self.p = micmcSettings['p']
        self.k = micmcSettings['k']
        self.c_values = micmcSettings['c']
        self.nRounds = micmcSettings['n']
    
    def __feistel(self, inL, inR, k):
        lastL, lastR = inL, inR
        
        for i in range(self.nRounds):
            mask = (lastR + k + self.c_values[i]) % self.p
            mask5 = pow(mask, 5, self.p)
            
            lastL, lastR = lastR, (lastL + mask5) % self.p
        
        return lastL, lastR
    
    def hash(self, m):
        lastR = lastC = 0
        for i in range(len(m)):
            lastR = (lastR + m[i]) % self.p
            lastR, lastC = self.__feistel(lastR, lastC, self.k)
        
        return lastR
