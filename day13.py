# part 1

lines = open(INPUT_FILE).readlines()
my_arrival = int(lines[0])
bus_ids = sorted(map(int, filter(lambda v: v != "x", lines[1].split(","))), key = lambda v : v - my_arrival % v)
print(bus_ids[0] * (bus_ids[0] - my_arrival % bus_ids[0]))

# part 2

INPUT_FILE = "example1"
lines = open(INPUT_FILE).readlines()
departure_ids = [
    (int(v), (int(v) - i) % int(v))
    for i, v in enumerate(lines[1].split(","))
    if v != "x"
]

i = 0
k = departure_ids[i][0]
increment = k
while True:
    div, mod = departure_ids[i + 1]
    if k % div == mod:
        if i == len(departure_ids) - 2:
            print(k)
            break
        increment *= div
        i += 1
    k += increment
