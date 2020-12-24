# https://www.redblobgames.com/grids/hexagons/
def move(coords, d):
    x, y, z = coords
    assert x + y + z == 0 and d in ["e", "w", "se", "sw", "ne", "nw"]
    if d == "e":
        return (x + 1, y - 1, z)
    if d == "w":
        return (x - 1, y + 1, z)
    if d == "ne":
        return (x + 1, y, z - 1)
    if d == "nw":
        return (x, y + 1, z - 1)
    if d == "se":
        return (x, y - 1, z + 1)
    if d == "sw":
        return (x - 1, y, z + 1)


def parse_line(l):
    steps = []
    l = list(l.strip())
    while len(l) > 0:
        c = l.pop(0)
        if c not in 'we':
            c += l.pop(0)
        steps.append(c)
    return steps
    

def get_neighbors(coords):
    return [move(coords, d) for d in ["e", "w", "se", "sw", "ne", "nw"]]


# part 1

tiles_are_flipped = dict()

INPUT_FILE = "input"

for line in open(INPUT_FILE):
    steps = parse_line(line)
    coord = (0,0,0)
    for step in steps:
        coord = move(coord, step)
    is_flipped = tiles_are_flipped.get(coord, False)
    tiles_are_flipped[coord] = not is_flipped

print(sum(v for v in tiles_are_flipped.values() if v))

# part 2

for _ in range(100):
    for coord in list(tiles_are_flipped):
        neighbors = get_neighbors(coord)
        for ncoord in neighbors:
            if ncoord not in tiles_are_flipped:
                tiles_are_flipped[ncoord] = False

    new_tiles = dict()
    for coord, is_flipped in tiles_are_flipped.items():
        flip_count = len([ncoord for ncoord in get_neighbors(coord) if tiles_are_flipped.get(ncoord, False)])
        if is_flipped and (flip_count == 0 or flip_count > 2):
            is_flipped = False
        elif not is_flipped and flip_count == 2:
            is_flipped = True
        new_tiles[coord] = is_flipped

    tiles_are_flipped = new_tiles
print(sum(v for v in tiles_are_flipped.values() if v))


