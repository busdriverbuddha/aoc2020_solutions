# Part 1

import re
pat1 = re.compile(r"mask = ([X01]+)")
pat2 = re.compile(r"mem\[(\d+)\] = (\d+)")

INPUT_FILE = "input"

bitmask = None # it is guaranteed that it will be set beforehand
memory = dict()

for line in open(INPUT_FILE):
    m1 = pat1.match(line)
    if m1:
        bitmask = m1.groups()[0]
        continue

    index, value = pat2.match(line).groups()
    memory[index] = "".join(
        (c if d == "X" else d)
        for c, d in zip("{:036b}".format(int(value)), bitmask)
    )
    
print(sum(int(v, 2) for v in memory.values()))


# Part 2

import re
pat1 = re.compile(r"mask = ([X01]+)")
pat2 = re.compile(r"mem\[(\d+)\] = (\d+)")

INPUT_FILE = "input"

all_binaries = lambda n: [list(("{:0" + str(n) + "b}").format(v)) for v in range(2**n)]

def replace_x(s):
    addresses = []
    n = s.count("X")
    for binary_string in all_binaries(n):
        new_string = ""
        for c in s:
            if c == "X":
                new_string += binary_string.pop(0)
            else:
                new_string += c
        addresses.append(new_string)
    return addresses

memory = dict()
bitmask = None

for line in open(INPUT_FILE):
    m1 = pat1.match(line)
    if m1:
        bitmask = m1.groups()[0]
        continue
    index, value = pat2.match(line).groups()
    new_index = "".join(
        (c if m == "0" else m)
    for c, m in zip("{:036b}".format(int(index)), bitmask)
    )
    indices = replace_x(new_index)
    for i in indices:
        memory[i] = value

print(sum(int(v) for v in memory.values()))



