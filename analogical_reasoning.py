import requests
import json
import syn_retriever as synretr
import similarity as sim

# Change color of outputs https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python?rq=1
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Text database containing words divided by type
with open("adjective_types.json", "r") as read_file:
    wordsdb = json.load(read_file)

# For each category of adjectives, the first and the second example adjectives in the list are the extremes (the bases for the precisiation step). These are retireved using the findextremes.py script.
# NOTE: Findextremes.py could be used at startup to compute each time the bases of each category, but to reduce execution time, we decided to store the resuts from findextremes.py this way.
maxes = {key: val[0] for key, val in wordsdb.items()}
mins = {key: val[1] for key, val in wordsdb.items()}

sr = synretr.SynDB("all_relevance.txt")

'''
#
# Conceptual analogies
#
'''

# Get relation type between two words
# Returns a tuple containing at pos 0 the relations from the first word to the second, and at pos 1 the relations from the second word to the first
def conceptnet_getrelations(w1, w2):
    wo1 = "/c/en/" + w1
    wo2 = "/c/en/" + w2
    
    # Get all relations from wo1 to wo2
    obj = requests.get("http://api.conceptnet.io/query?start=" + wo1 + "&end=" + wo2).json()
    rel = [o["rel"]["@id"] for o in obj["edges"]]
    
    # Get all relations from wo2 to wo1
    obj_inv = requests.get("http://api.conceptnet.io/query?start=" + wo2 + "&end=" + wo1).json()
    rel_inv = [o["rel"]["@id"] for o in obj_inv["edges"]]
    
    rel, rel_inv = remove_relatedTo(rel, rel_inv) # Remove RelatedTo, if another relation exists, to avoid a lot of unnecessary answer options
    return clean_relations(rel, rel_inv) # Remove duplicates and bidirectional relations
    
    
# Get all words related to the input word by the relation rel
def conceptnet_getrelatedwords(w, rel, rel_inv):
    wo = "/c/en/" + w
    res = ([], [])
    for rela in rel:
        obj = requests.get("http://api.conceptnet.io/query?start=" + wo + "&rel=" + rela).json()
        res[0].append([r["end"]["label"] for r in obj["edges"]])
    
    for rela_inv in rel_inv:
        obj = requests.get("http://api.conceptnet.io/query?end=" + wo + "&rel=" + rela_inv).json()
        res[1].append([r["start"]["label"] for r in obj["edges"]])
    
    return res

'''
#
# Spectral analogies
#
'''
# Get most probable category of adjectives - Improved to exploit the fact that several adjectives should belong to the same category
def get_category(adjectives_list):
    for k,v in wordsdb.items():
        if all([w in v for w in adjectives_list]):
            return k
    # Using lvl1 synonyms if words are not in the list
    syns = flatten([s for w in adjectives_list for s in sr.retrieve_syn(w)])
    overlaps = {k: sim.count_overlaps(syns,v) for (k, v) in wordsdb.items()}
    return max(overlaps, key=overlaps.get)


# Get (non-oriented, for first test) similarity between two words
def adj_similarity(w1, w2):
    return sim.sim_lvl2(w1, w2)

# Get NON-ORIENTED (abs, otherwise remove it) similarity between words
# Why non-oriented? -> To allow "negative" analogies, like (small, expensive):(big, cheap)
# BUT, when adjectives which are not on the extremes are used, then the result *might* be wrong
# TODO: possible solution: when adj far from the extremes, then take abs, otherwise not -> But it has first to be tested if this is the expected behavior or not (!!)
def norm_distance(w1, w2, category, verbose = False):
    w1p, w2p = precisiation(w1, category), precisiation(w2, category)
    
    if verbose:
        display_precisiated_values(w1, w1p, w2, w2p)
    
    return abs(w1p - w2p)

# Precisiate the meaning of a the word w, knowing the category to which it belongs, using level 2 similarity
def precisiation(w, category):
    maxsim = sim.sim_lvl2(w, maxes[category])
    minsim = sim.sim_lvl2(w, mins[category])
    return (maxsim*1+minsim*0)/(maxsim + minsim)

# Get element of type t related to a word of type t in the most similar way as relation rel
def norm_getmostrelatedword(w, t, rel):
    temp = [(abs(norm_distance(w, wi, t)-rel), wi) for wi in wordsdb[t]]
    best = min(temp)
    
    return best
    
    
'''
#
# Helpers
#
'''

# Flatten a 2d list
def flatten(list2d):
    return [el for sublist in list2d for el in sublist]
    
# Remove RelatedTo if there are other relations in a list
def remove_relatedTo(lst1, lst2):
    if any(el != "/r/RelatedTo" for el in lst1 + lst2):
        return ([li for li in lst1 if li != "/r/RelatedTo"], [li for li in lst2 if li != "/r/RelatedTo"])
    else:
        return (lst1, lst2)
        
# Remove duplicates and bidirectional relations
def clean_relations(lst1, lst2):
    # Remove duplicates
    lst1 = list(set(lst1))
    lst2 = list(set(lst2))
    
    # Remove bidirectional relations (keep only one direction)
    lst2 = [li for li in lst2 if li not in lst1 ]
    
    return (lst1, lst2)
    
# Display precisiated values of words
def display_precisiated_values(w1, w1p, w2, w2p):
    pattern = "|------------------------------|"
    
    print(f"Precisiated value of {bcolors.OKBLUE}{w1}{bcolors.ENDC} (defuzzified): {bcolors.OKBLUE}{w1p}{bcolors.ENDC}")
    print(f"Precisiated value of {bcolors.OKGREEN}{w2}{bcolors.ENDC} (defuzzified): {bcolors.OKGREEN}{w2p}{bcolors.ENDC}")
    
    if w2p > w1p:
        pos1 = int(w1p*30+1)
        pos2 = int(w2p*30+1)
        print(f"{pattern[:pos1]}{bcolors.OKBLUE}X{bcolors.ENDC}{pattern[pos1+1:pos2]}{bcolors.OKGREEN}X{bcolors.ENDC}{pattern[pos2+1:]}\n")
    else:
        pos1 = int(w1p*30+1)
        pos2 = int(w2p*30+1)
        print(f"{pattern[:pos2]}{bcolors.OKGREEN}X{bcolors.ENDC}{pattern[pos2+1:pos1]}{bcolors.OKBLUE}X{bcolors.ENDC}{pattern[pos1+1:]}\n")
