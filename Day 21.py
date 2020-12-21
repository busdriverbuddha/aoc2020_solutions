#!/usr/bin/env python
# coding: utf-8

import re

INPUT_FILE = "input"
pat = re.compile(r"^([a-z\s]+) \(contains ([a-z,\s]+)\)$")

ingredients = []
allergen_reference = dict()
for i, line in enumerate(open(INPUT_FILE)):
    ing, allerg = pat.match(line).groups()
    ingredients.append(ing.split())
    for al in allerg.split(", "):
        this_list = allergen_reference.get(al, list())
        this_list.append(i)
        allergen_reference[al] = this_list

allergen_candidates = {
    key: set.intersection(*[set(ingredients[k]) for k in allergen_reference[key]])
    for key, value in allergen_reference.items()
}

no_ingredient = set(i for l in ingredients for i in l).difference(set.union(*(allergen_candidates.values())))

# part 1
print(len([i for l in ingredients for i in l if i in no_ingredient]))

visited = set()
while any(len(s) > 1 for s in allergen_candidates.values()):
    for key, value in allergen_candidates.items():
        if len(value) == 1 and key not in visited:
            visited.add(key)
            break
    for key2, value2 in allergen_candidates.items():
        if key2 != key:
            value2.difference_update(value)
    
        
# part 2
print(",".join(next(iter(v)) for _, v in sorted(allergen_candidates.items(), key=lambda v: v[0])))






