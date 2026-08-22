## Summary

Demonstrate the actor model by implementing domain logic to solve sudoku puzzles.

## Actors

### Controller

![alt](https://github.com/sunlao/py_sudoku_solver/blob/main/docs/diagrams/ControllerActor.svg)

#### Description

The Controller manages the domain actor's lifecycle. Recieves update messages from domain actors and pushes them to the framework administrator.

#### Message Spec

- Start-up
- Update Domain Actor Status

#### Static info

- List of actors with attributes and the associated cell id's for RBC acttors

### Game

![alt](https://github.com/sunlao/py_sudoku_solver/blob/main/docs/diagrams/GameActor.svg)

#### Description

The Game actor manages the game lifecycle and initializes RBC and Board actors.

#### Message Spec

- Start Gagem
- Cell Update

#### Static info

- controller address

### RBC

![alt](https://github.com/sunlao/py_sudoku_solver/blob/main/docs/diagrams/RBCActor.svg)

#### Description

The RBC actor manages one row, box, or column set.

#### Message Spec

- Initialize
- Cell Update

#### Algorithms

- Naked Single
- Hidden Single
- Naked Pair
- Hidden Pair
- Naked Triple
- Hidden Triple

#### Static info

- association of RBC set to shared cells with other RBC Actors
- controller address

### Board

![alt](https://github.com/sunlao/py_sudoku_solver/blob/main/docs/diagrams/BoardActor.svg)

#### Description

The Board actor manages the board and runs algorithms that require board-level visibility.

#### Message Spec

- Initialize

#### Algorithms

- X-Wing
- Swordfish
- Jellyfish
- YWing
- XYZ-Wing
- Simple Coloring
- Multi-Coloring
- XY-Chain
- Forcing Chains
- Unique Rectangle
- Pointing Pair / Pointing Triple
- Box-Line Reduction

#### Static info

- controller address
