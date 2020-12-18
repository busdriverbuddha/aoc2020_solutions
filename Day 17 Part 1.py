def print_space(space):
    X, Y, Z = zip(*space.keys())
    for k in sorted(set(Z)):
        print("z={:d}".format(k))
        for i in sorted(set(Y)):
            for j in sorted(set(X)):
                print(space[(j, i, k)], end="")
            print()
        print()
    

def add_shell(space):
    X, Y, Z = zip(*space.keys())
    x1, x2 = min(X), max(X)
    y1, y2 = min(Y), max(Y)
    z1, z2 = min(Z), max(Z)
    for j in range(x1 - 1, x2 + 2):
        for i in range(y1 - 1, y2 + 2):
            for k in range(z1 - 1, z2 + 2):
                coord = (j, i, k)
                if coord not in space:
                    space[coord] = "."


def get_neighbors(x, y, z):
    return [
        (j, i, k)
        for j in range(x-1, x+2)
        for i in range(y-1, y+2)
        for k in range(z-1, z+2)
        if j != x or i != y or k != z
    ]


def next_state(space):
    new_space = dict()
    add_shell(space)
    for coord, value in space.items():
        active_neighbors = 0
        for n_coords in get_neighbors(*coord):
            if space.get(n_coords, ".") == "#":
                active_neighbors += 1
        if (value == "#" and 2 <= active_neighbors <= 3
            or value == "." and active_neighbors == 3):
            new_value = "#"
        else:
            new_value = "."
        new_space[coord] = new_value
    return new_space
        

INPUT_FILE = "input"
grid = [list(line.strip()) for line in open(INPUT_FILE)]
shift = (1 - len(grid)) // 2
space = {
    (j + shift, i + shift, 0) : grid[i][j]
    for i in range(len(grid))
    for j in range(len(grid[i]))
}

for _ in range(6):
    space = next_state(space)

print(list(space.values()).count("#"))
