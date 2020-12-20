#!/usr/bin/env python
# coding: utf-8

import re
from collections import deque

def make_binary(s):
    trans_table = s.maketrans(".#", "01")
    new_s = s.translate(trans_table)
    return int(new_s, 2)

def make_text(s):
    trans_table = s.maketrans("01", ".#")
    new_s = s.translate(trans_table)
    return new_s


def flip_binary(n):
    return int("".join(list("{:010b}".format(n))[::-1]), 2)

def get_edges(M):
    north = "".join(M[0])
    south = "".join(M[-1][::-1])
    west = "".join(row[0] for row in M[::-1])
    east = "".join(row[-1] for row in M)
    return deque([north, east, south, west])
    

class Tile:
    def __init__(self, tilestring=None, tile_id=None, edges=None, moves=[]):
        if tilestring is not None:
            lines = tilestring.strip().split("\n")
            self.id = int(re.match(r"Tile (\d+):", lines[0]).groups()[0])
            self.edges = get_edges(lines[1:])
        elif id is not None and edges is not None:
            self.id = tile_id
            self.edges = edges
        self.moves = moves
        self._get_all_edges()
        
        
    def __repr__(self):
        return "Tile({:d}, {:s})".format(self.id, " ".join(str(make_binary(e)) for e in self.edges))
    
    def _get_all_edges(self):
        self.all_edges = set(self.edges)
        self.flip()
        self.all_edges.update(self.edges)
        self.flip()
    
    def rotate(self):
        self.edges.rotate()
        self.moves.append("r")
        
    def flip(self):
        self.edges = deque(
        [
            self.edges[2][::-1], # north
            self.edges[1][::-1], # east
            self.edges[0][::-1], # south
            self.edges[3][::-1], # west
        ]
        )
        self.moves.append("f")
        
    def is_match(self, other, d):
        if d == "E":
            return self.edges[1] == other.edges[3][::-1]
        if d == "W":
            return self.edges[3] == other.edges[1][::-1]
        if d == "N":
            return self.edges[0] == other.edges[2][::-1]
        if d == "S":
            return self.edges[2] == other.edges[0][::-1]
        
    def copy(self):
        return Tile(tile_id=self.id, edges=deque(self.edges), moves=self.moves[:])
        
    def pprint(self):
        print("""    {:3d}
{:3d}     {:3d}
    {:3d}
        """.format(
            make_binary(self.edges[0]), 
            make_binary(self.edges[3]),
            make_binary(self.edges[1]), 
            make_binary(self.edges[2])))
    
    def printgrid(self):
        b_edges = self.edges
        s = b_edges[0] + "\n"
        for i in range(1,10):
            s += b_edges[3][10-i] + 8 * " " + b_edges[1][i] + "\n"
        s += b_edges[2][::-1]
        print(make_text(s))

def get_all_rotations(t):
    rotations = []
    t = t.copy()
    for _ in range(4):
        t = t.copy()
        t.rotate()
        rotations.append(t)
        
    return rotations

def get_all_variations(t):
    t = t.copy()
    variations = get_all_rotations(t)
    t.flip()
    variations += get_all_rotations(t)
    return variations



INPUT_FILE = "input"
from timeit import default_timer as timer


from math import sqrt
N = 0 # used as a global for the size of the puzzle

def move(i, j, d):
    if d == "N" and i > 0:
        return (i - 1, j)
    if d == "E" and j < N - 1:
        return (i, j + 1)
    if d == "W" and j > 0:
        return (i, j - 1)
    if d == "S" and i < N - 1:
        return (i + 1, j)
    
def get_neighbors(i, j):
    neighbors = dict()
    for d in "N E S W".split():
        if (coord := move(i, j, d)) is not None:
            neighbors[d] = coord
            
    return neighbors

tiles = open(INPUT_FILE).read().split("\n\n")
N = int(sqrt(len(tiles)))

T = [Tile(t) for t in tiles]
full_tile_set = {
    t.id: get_all_variations(t)
    for t in T
}

def solve():

    path = [(i, j) for i in range(N) for j in range(N)]
    grid = [[None for _ in range(N)] for _ in range(N)]
    unused_ids = list(full_tile_set.keys())
    step = 0

    starting_problem = {
        'step': step,
        'grid': grid,
        'unused_ids': unused_ids,
    }

    stack = [starting_problem]

    while stack:
        p = stack.pop()
        step = p['step']
        grid = p['grid']
        unused_ids = p['unused_ids']
        if step == len(path): # success
            return p['grid']
        
        u, v = path[step]
        # print(u, v)

        for tileid in unused_ids:
            a = 1
            for tilevar in full_tile_set[tileid]:
                tile_fits = True
                for d, (n_i, n_j) in get_neighbors(u, v).items():
                    if (neighbortile := grid[n_i][n_j]) is not None:
                        if not tilevar.is_match(neighbortile, d):
                            tile_fits = False
                            break

                if not tile_fits:
                    continue

                new_grid = [row[:] for row in grid]
                new_grid[u][v] = tilevar
                new_unused_ids = unused_ids[:]
                new_unused_ids.remove(tileid)
                new_problem = {
                    'step': step + 1,
                    'grid': new_grid,
                    'unused_ids': new_unused_ids
                }
                stack.append(new_problem)


# part 1

start = timer()
g = solve()
print("{:.02f}s".format(timer() - start))
print(
    g[0][0].id * g[0][-1].id * g[-1][0].id * g[-1][-1].id
)

# part 2. We start by recreating the image because in part 1 we stored only the edges

instructions = [[(t.id, t.moves) for t in row] for row in g]

all_tiles = dict()
for tile in open(INPUT_FILE).read().split("\n\n"):
    lines = tile.split("\n")
    tileid = int(re.match(r"Tile (\d+):", lines[0]).groups()[0])
    image = lines[1:]
    image = [list(row[1:-1]) for row in image[1:-1]]
    all_tiles[tileid] = image

def rotate(A):
    A = [row[:] for row in A]
    N = len(A[0])
    for i in range(N // 2):
        for j in range(i, N - i - 1):
            temp = A[i][j]
            A[i][j] = A[N - 1 - j][i]
            A[N - 1 - j][i] = A[N - 1 - i][N - 1 - j]
            A[N - 1 - i][N - 1 - j] = A[j][N - 1 - i]
            A[j][N - 1 - i] = temp
            
    return A

def flip(A):
    return A[::-1]

def image2string(A):
    return ["".join(row) for row in A]

full_image = []
for instruction_row in instructions:
    this_row = []
    for tileid, moves in instruction_row:
        this_image = all_tiles[tileid]
        for m in moves:
            if m == "r":
                this_image = rotate(this_image)
            elif m == "f":
                this_image = flip(this_image)
        this_row.append(this_image)
    full_image.append(this_row)

consolidated_image = []
for row in full_image:
    consolidated_rows = [list() for _ in range(8)]
    for piece in row:
        for i in range(8):
            consolidated_rows[i] += piece[i]
    consolidated_image += consolidated_rows
    

monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.replace(" ", "0").replace("#", "1").splitlines()
monster_coords = [(i,j) for i in range(len(monster)) for j in range(len(monster[i])) if monster[i][j] == "1"]
monster = [int(row, 2) for row in monster]


# here I had intended to manually rotated and/or flipped until I got the proper image
# but I got lucky and got the right image from the start
test_image = consolidated_image

found_coords = list()
for i in range(len(test_image) - 2):
    for j in range(len(test_image[i]) - 19):
        this_slice = [make_binary("".join(row[j:j+20])) for row in test_image[i:i+3]]
        compares = [
            (slicerow | monsterrow) == slicerow
            for slicerow, monsterrow in zip(this_slice, monster)
        ]
        if all(compares):
            for u, v in monster_coords:
                found_coords.append((i+u, j+v))

# part 2

print(sum(row.count("#") for row in test_image) - len(found_coords))
