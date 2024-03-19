from hashlib import sha256

class MerkleTree:
    def __init__(self, depth):
        self.depth = depth
        self.zero_roots = list()
        self.__set_zero_roots()
        self.__tree = [[] for i in range(depth)]
        self.__current_insert_idx = 0
    
    def hash_data(self, data=None):
        return sha256(data.encode() if data else bytes(0)).hexdigest()
    
    def hash_lr(self, left, right):
        lr = hex(int(left, 16) + int(right, 16))[2: ]
        return self.hash_data(lr)
    
    def __set_zero_roots(self):
        t_hash = self.hash_data()
        self.zero_roots.append(t_hash)
        for i in range(1, self.depth):
            t_hash = self.hash_lr(t_hash, t_hash)
            self.zero_roots.append(t_hash)
    
    def is_tree_full(self):
        return True if self.__current_insert_idx >= 2 ** (self.depth - 1) else False
    
    def insert_leaf(self, data):
        if self.is_tree_full():
            print("Merkle Tree is Full.")
            return
        
        curr_idx = self.__current_insert_idx
        curr_hash = self.hash_data(data)
        self.__tree[0].append(curr_hash)
        for i in range(1, self.depth):
            next_idx = curr_idx // 2
            if curr_idx % 2 == 0: # even -> left child
                l = curr_hash
                r = self.zero_roots[i - 1]
            else: # odd -> right child
                l = self.__tree[i - 1][curr_idx - 1]
                r = curr_hash
            
            curr_idx = next_idx
            curr_hash = self.hash_lr(l, r)
            if len(self.__tree[i]) <= next_idx: self.__tree[i].append(curr_hash)
            else: self.__tree[i][curr_idx] = curr_hash 
        
        self.__current_insert_idx += 1
    
    def get_root(self):
        return self.__tree[-1][0] if len(self.__tree[-1]) == 1 else self.zero_roots[-1]
    
    def get_leaf_index(self, data):
        leaf_hash = self.hash_data(data)
        return self.__tree[0].index(leaf_hash) if leaf_hash in self.__tree[0] else -1
