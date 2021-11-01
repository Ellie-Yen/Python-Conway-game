'''
Elie Yen
Conway's Game of life
v 2.0
python 3.8

rule:
Any live cell with fewer than 2 live neighbours dies, as if by underpopulation.
Any live cell with 2 or 3 live neighbours lives on to the next generation.
Any live cell with more than 3 live neighbours dies, as if by overpopulation.
Any dead cell with exactly 3 live neighbours becomes a live cell, as if by reproduction

ref: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
'''
import numpy
import math
from typing import List, Tuple

#_ the direction of adjacent cells
adj_rule = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),
           (1, -1), (1, 0), (1, 1)]

def game_run(cells: 'List[List[int]]', generation: int) -> str:
    if generation < 0:
        return f'invalid generation {generation}'

    print(f'\ngeneration {0}\n', cells)
    for i in range(1, generation + 1):
        cells = get_next_generation(cells, adj_rule)
        print(f'\ngeneration {i}\n', cells)

    return 'end'

def get_next_generation(cells: 'List[List[int]]', adj_rule: 'List[Tuple[int]]') -> 'List[List[int]]':
    if len(cells) < 1:
        return cells
    
    h, w = len(cells), len(cells[0])

    #_ expand 1 cells in each border
    next_cells: List[List[int]] = numpy.zeros(
        shape = (h + 2, w + 2), 
        dtype = numpy.int8
    )

    #_ mark neighbors by 2
    #_ thus we can tell it's original live or dead.
    for row in range(1, h + 1):
        for col in range(1, w + 1):
            r, c = row - 1, col - 1
            if not cells[r][c]:
                continue
            
            next_cells[row][col] += 1
            for x, y in adj_rule:
                next_cells[row + x][col + y] += 2

    #_ the left top and right bottom edge to crop
    left, right = w + 2, 0
    top, bottom = h + 2, 0
    has_live = False

    for row in range(h + 2):
        for col in range(w + 2): 
            if next_cells[row][col] < 5 or next_cells[row][col] > 7:
                next_cells[row][col] = 0

            #_ 5, 7: original live cells surrounded by 2 / 3 cells ( 1 + 2 * 2, 1 + 2 * 3)
            #_ 6: original dead cells surrounded by 3 cells (0 + 2 * 3)
            else:
                next_cells[row][col] = 1
                has_live = True
                left, right = min(left, col), max(right, col)
                top, bottom = min(top, row), max(bottom, row)
    
    if not has_live:
        return [[0]]
    
    return next_cells[top: (bottom + 1), left: (right + 1)]

def __main__():
    cells = numpy.random.randint(2, size=(6, 10))
    game_run(cells, 5)

__main__()