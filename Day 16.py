import re
from sympy import Interval, Union

f = open("input")

pat1 = re.compile(r"([a-z ]+): (\d+)\-(\d+) or (\d+)\-(\d+)")


class MyInterval:
    '''Meant to replace sympy's Interval
    which has a super slow __contains__ for some reason'''
    def __init__(self, a1, b1, a2, b2):
        self.a1 = a1
        self.a2 = a2
        self.b1 = b1
        self.b2 = b2
        
    def __contains__(self, v):
        return self.a1 <= v <= self.b1 or self.a2 <= v <= self.b2
    
    def __repr__(self):
        return "MyInterval({:d}, {:d}, {:d}, {:d})".format(self.a1, self.b1, self.a2, self.b2)


fields = dict()
intervals_for_union = []
while True:
    line = f.readline()
    m = pat1.match(line)
    if m:
        field = m.groups()[0]
        a1, b1, a2, b2 = map(int, m.groups()[1:])
        intervals_for_union.append(Interval(a1, b1))
        intervals_for_union.append(Interval(a2, b2))
        field_intvl = MyInterval(a1, b1, a2, b2)
        fields[field] = field_intvl
    else:
        break

u = Union(*intervals_for_union)

# your ticket
f.readline()
your_ticket = list(map(int, f.readline().split(",")))
f.readline()
f.readline()
    
# get nearby tickets and find answer to part 1
nearby_tickets = []
rejected_value_sum = 0

while True:
    line = f.readline()
    if not line:
        break
    values = list(map(int, line.split(",")))
    rejected_values = list(filter(lambda v: v not in u, values))
    if rejected_values:
        rejected_value_sum += sum(rejected_values)
    else:
        nearby_tickets.append(values)
    
# part 1 solution
print(rejected_value_sum)

# we transpose the matrix of all tickets to get all the values for each field
all_tickets = [your_ticket] + nearby_tickets
values_by_field = [set(all_tickets[j][i] for j in range(len(all_tickets))) for i in range(len(all_tickets[0]))]

# we get all the possible column indices for each field
candidates = {key: list() for key in fields}
for fieldname in candidates:
    print(fieldname)
    for i, this_set in enumerate(values_by_field):
        if all(v in fields[fieldname] for v in this_set):
            candidates[fieldname].append(i)
            
# we match each index to each field by elimination
results = dict()
done = False
while not done:
    done = True
    for key, value in candidates.items():
        if len(value) > 0:
            done = False
            if len(value) == 1:
                found_candidate = value[0]
                results[key] = found_candidate
                candidates[key] = list()
                for value2 in candidates.values():
                    if found_candidate in value2:
                        value2.remove(found_candidate)
                
        
        
my_ticket_values = {key: your_ticket[value] for key, value in results.items() if key.startswith('departure')}.values()
p = 1
for v in my_ticket_values:
    p *= v

# part 2 solution
print(p)