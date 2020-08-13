import json
import similarity as sim
import numpy as np
from itertools import combinations
import timeit

# Text database containing words divided by type
with open("adjective_types.json", "r") as read_file:
    wordsdb = json.load(read_file)

for k,lst in wordsdb.items():
    comb = list(combinations(lst, 2))

    t = [sim.sim_lvl2(cp[0], cp[1]) for cp in comb]
    res = comb[np.argmin(t)]
    #res = [sim_l3(cp[0], cp[1]) for cp in comb]

    print(str(res))


