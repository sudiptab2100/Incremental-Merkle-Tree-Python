from hashlib import sha256
import pickle


class IncrementalMerkleTree:
    def __init__(self, depth, load_from_file=False, file_path='files/merkle_tree.pkl'):
        if load_from_file:
            try:
                with open(file_path, 'rb') as f:
                    loaded_tree = pickle.load(f)
                self.depth = loaded_tree.depth
                self.zero_roots = loaded_tree.zero_roots
                self.__tree = loaded_tree.__tree
                self.__current_insert_idx = loaded_tree.__current_insert_idx
            except FileNotFoundError:
                print(f"No such file: '{file_path}'")
                return
            except Exception as e:
                print(f"Error loading tree from file: {e}")
                return
        else:
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
    
    def get_node(self, level, idx):
        if not 0 <= level < self.depth:
            print("Invalid Level")
            return
        if not 0 <= idx < 2 ** (self.depth - level - 1):
            print("Invalid Index")
            return
        
        node_value = self.__tree[level][idx] if len(self.__tree[level]) > idx else self.zero_roots[level]
        return node_value
    
    def get_leaf(self, leaf_idx):
        if not 0 <= leaf_idx < 2 ** (self.depth - 1):
            print("Invalid Index")
            return
        
        return self.__tree[0][leaf_idx] if len(self.__tree[0]) > leaf_idx else self.zero_roots[0]
    
    def get_path(self, leaf_idx):
        if not 0 <= leaf_idx < 2 ** (self.depth - 1):
            print("Invalid Index")
            return
        
        path = []
        curr_idx = leaf_idx
        for i in range(self.depth - 1):
            if curr_idx % 2 == 0: # even -> left child
                neigh_idx = curr_idx + 1
            else: # odd -> right child
                neigh_idx = curr_idx - 1
            
            neigh = self.__tree[i][neigh_idx] if len(self.__tree[i]) > neigh_idx else self.zero_roots[i]
            path.append(neigh)
            curr_idx = curr_idx // 2 # parent index
        
        return path
    
    def is_tree_member(self, leaf, path):
        if len(path) != self.depth - 1:
            print("Invalid Path")
            return
        
        root = leaf
        for p in path:
            root = self.hash_lr(root, p)
        
        return root == self.get_root()
    
    def store_tree(self, loc='files/merkle_tree.pkl'):
        with open(loc, 'wb') as f:
            pickle.dump(self, f)
