# Incremental Merkle Tree (IMT) - Python

Incremental Merkle Tree is a specialized form of a Merkle tree designed to allow for efficient appending of new elements, making it useful in applications where the dataset is expected to grow over time and updates need to be processed efficiently.

## Advantages

- ### Efficiency
    New elements can be appended without recomputing the entire tree.
- ### Consistent Growth
    The structure can grow dynamically as new elements are added, making it suitable for scenarios where the dataset size isn't fixed.
- ### Proofs
    Similar to traditional Merkle trees, the IMT allows for the creation of Merkle proofs, which prove the inclusion of a particular element in the tree without revealing other elements.

## Code

- #### `prog.py`
    Incremental Merkle Tree class implemented with all the functionalities.
- #### `MiMC5Sponge.py`
    Implementation of MiMC5Sponge hasher. MiMC is a hash function family specially designed for SNARK applications. The low multiplicative complexity of MiMC over prime fields makes it suitable for ZK-SNARK applications
- ### `files/MiMC_settings.json`
    It includes the parameters for MiMC implementation.