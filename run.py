from prog import IncrementalMerkleTree

m = IncrementalMerkleTree(20)
for i in range(30):
    m.insert_leaf(str(i))

idx = 13
leaf = m.get_leaf(idx)
path = m.get_path(idx)

# print(leaf)
# print()
# for p in path: print(p)

# p = [x[1] for x in path]
# ttt = m.is_tree_member(leaf, p)
# print(ttt)

rootC = leaf
for p in path:
    side, h = p
    if side == 0:
        rootC = m.hash_lr(h, rootC)
    else:
        rootC = m.hash_lr(rootC, h)
print(rootC)
print(m.get_root())
print(m.is_tree_member(leaf, path))