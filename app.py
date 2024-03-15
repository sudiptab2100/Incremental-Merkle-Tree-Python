from hashlib import sha256

class MerkleTree:
    def __init__(self, depth):
        self.depth = depth
        self.zero_roots = list()
        self.__set_zero_roots()
    
    def hash_data(self, data=None):
        return sha256(data.encode() if data else bytes(0)).hexdigest()
    
    def hash_lr(self, left, right):
        return self.hash_data(left + right)
    
    def __set_zero_roots(self):
        t_hash = self.hash_data()
        self.zero_roots.append(t_hash)
        for i in range(1, self.depth):
            t_hash = self.hash_lr(t_hash, t_hash)
            self.zero_roots.append(t_hash)
