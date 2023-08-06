![example workflow](https://github.com/michalskibinski109/checkers/actions/workflows/python-app.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/fast_checkers.svg)](https://badge.fury.io/py/fast_checkers)

# Checkers 

__Project still under active development. Usage may be different in futurue versions__

Efficient Modern and flexible implementation of checkers game with beautiful web interface.
Supports multiple variants of the game and allows to play against AI.

# Installation

```bash
python -m pip install fast-checkers 
```

## Usage:

### simple

```python
import checkers.american as checkers
board = checkers.Board()
move = checkers.Move([checkers.A3, checkers.B4])
board.push(move)

print(list(board.legal_moves))
print(board)
```

```bash
['Move through squares: [8, 12]', 'Move through squares: [8, 13]', 'Move through squares: [9, 13]', 'Move through squares: [9, 14]', 'Move through squares: [10, 14]', 'Move through squares: [10, 15]', 'Move through squares: [11, 15]']
---------------------------------
|   | x |   | x |   | x |   | x |
---------------------------------
| x |   | x |   | x |   | x |   |
---------------------------------
|   | x |   | x |   | x |   | x |
---------------------------------
|   |   |   |   |   |   |   |   |
---------------------------------
|   |   |   | o |   |   |   |   |
---------------------------------
| o |   |   |   | o |   | o |   |
---------------------------------
|   | o |   | o |   | o |   | o |
---------------------------------
| o |   | o |   | o |   | o |   |
```

### advenced:

```python
import checkers.base as checkers
import numpy as np
CUSTOM_POSITION = np.array([1] * 20 + [-1] * 12, dtype=np.int8)
board = checkers.BaseBoard(starting_position=CUSTOM_POSITION)
board.legal_moves = ... # create your own custom legal_moves method (property)
print(board)
print(board.legal_moves)
```

```bash
---------------------------------
|   | x |   | x |   | x |   | x |
---------------------------------
| x |   | x |   | x |   | x |   |
---------------------------------
|   | x |   | x |   | x |   | x |
---------------------------------
| x |   | x |   | x |   | x |   |
---------------------------------
|   | x |   | x |   | x |   | x |
---------------------------------
| o |   | o |   | o |   | o |   |
---------------------------------
|   | o |   | o |   | o |   | o |
---------------------------------
| o |   | o |   | o |   | o |   |

Ellipsis
```


## Bibliography
1. [notatin](https://en.wikipedia.org/wiki/Portable_Draughts_Notation)
2. [rules and variants](https://en.wikipedia.org/wiki/Checkers)
3. [additional 1 (checkers online)](https://checkers.online/play)
4. [additional 2 (chinook)](https://webdocs.cs.ualberta.ca/~chinook/play/notation.html)

## Contributing

Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the project repository.

---

## ideas
Move can be stored as 
16 bits:
`0b 000000 00000 000000 0`
where:
- 0-6 bits - source square (0-63)
- 6-12 bits - destination square (0-63)
-  12-18 bits - captured piece (0-63)
- 19 bit - weather captured piece is king (0-1)
> bigest possible board is 10x10, so 6 bits is enough to store square number

