![example workflow](https://github.com/michalskibinski109/checkers/actions/workflows/python-app.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/fast_checkers.svg)](https://badge.fury.io/py/fast_checkers)

# Checkers 

__Project still under active development. Usage may be different in futurue versions__

Efficient Modern and flexible implementation of checkers game with beautiful web interface.
Supports multiple variants of the game and allows to play against AI.

## [Documentation](https://michalskibinski109.github.io/checkers/)

# Installation

```bash
python -m pip install fast-checkers 
```

## Usage:

### simple

```python
import checkers.american as checkers

board = checkers.Board()


board.push_from_str("24-19")
board.push_from_str("12-16")
board.push_from_str("23-18")
board.push_from_str("16x23")
board.push_from_str("26x19")
print(board)
```
```bash
---------------------------------
|   | x |   | x |   | x |   | x |
---------------------------------
| x |   | x |   | x |   | x |   |
---------------------------------
|   | x |   | x |   | x |   |   |
---------------------------------
|   |   |   |   |   |   |   |   |
---------------------------------
|   |   |   | o |   | o |   |   |
---------------------------------
| o |   | o |   |   |   |   |   |
---------------------------------
|   | o |   |   |   | o |   | o |
---------------------------------
| o |   | o |   | o |   | o |   |
```
```python
board.pop()
print(board)
```
```bash
---------------------------------
|   | x |   | x |   | x |   | x |
---------------------------------
| x |   | x |   | x |   | x |   |
---------------------------------
|   | x |   | x |   | x |   |   |
---------------------------------
|   |   |   |   |   |   |   |   |
---------------------------------
|   |   |   | o |   |   |   |   |
---------------------------------
| o |   | o |   | x |   |   |   |
---------------------------------
|   | o |   | o |   | o |   | o |
---------------------------------
| o |   | o |   | o |   | o |   |
```
```python
print(list(board.legal_moves))
```
```bash
[Move through squares: [8, 12], Move through squares: [9, 13],
 Move through squares: [9, 14], Move through squares: [10, 14],
 Move through squares: [10, 15], Move through squares: [11, 15],
 Move through squares: [11, 16]]
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
3. [list of pdns](https://github.com/mig0/Games-Checkers/)
4. [additional 1 (checkers online)](https://checkers.online/play)
5. [additional 2 (chinook)](https://webdocs.cs.ualberta.ca/~chinook/play/notation.html)

## UI
__for now UI is mostly used for debugging pruposes__


<img src="https://github.com/michalskibinski109/checkers/assets/77834536/acae0786-9cf3-4e30-9a04-abd7c018202b" width="400">

## Contributing

Contributions to this project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the project repository.

---

