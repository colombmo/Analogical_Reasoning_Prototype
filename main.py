import analogical_reasoning as ar
import re

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
    
verbose = True

pattern1 = re.compile("[A-Za-z_-]+:[A-Za-z_-]+::[A-Za-z_-]+:\?") # Pattern to be matched to express a conceptual analogy
pattern2 = re.compile("[A-Za-z_-]+\([A-Za-z_-]+, ?[A-Za-z_-]+\):[A-Za-z_-]+\([A-Za-z_-]+, ?\?\)") # Pattern to be matched to express a spectral analogy

inpt = input("Please input an analogy in one of the following forms: book:chapter::city:? OR A(big, expensive):B(small, ?)\n>")

### Analogical reasoning using conceptual analogies
if pattern1.match(inpt):
    w1 = inpt[:inpt.find(":")]
    w2 = inpt[inpt.find(":")+1:inpt.find("::")]
    v = inpt[inpt.find("::")+2:inpt.find(":?")]

    rela = ar.conceptnet_getrelations(w1, w2) # Get relation between w1 and w2
    print("")
    
    # Print the type of relations identified between the input words
    if verbose:
        for r in rela[0]:
            print(f"{w1} {bcolors.OKGREEN} {r[3:]} {bcolors.ENDC} {w2}")
        
        for r in rela[1]:
            print(f"{w2} {bcolors.OKGREEN} {r[3:]} {bcolors.ENDC} {w1}")
        
        print("")
            
    res = ar.conceptnet_getrelatedwords(v, rela[0], rela[1]) # Get words related to v as w2 is related to w1
    
    print(f"{w1} is to {w2} as {v} is to what?\n")
    
    # Format output
    for i, r in enumerate(res[0]):
        print(f"Using {bcolors.OKGREEN}{rela[0][i][3:]} {bcolors.ENDC} as relation: {bcolors.OKBLUE} {r} {bcolors.ENDC}")
    
    for i, r in enumerate(res[1]):
        print(f"Using {bcolors.FAIL}Opposite of {rela[1][i][3:]}{bcolors.ENDC} as relation: {bcolors.OKBLUE} {r} {bcolors.ENDC}")
    
    print("\n")

### Analogical reasoning using spectral analogies
elif pattern2.match(inpt):
    # Parse all important elements from input
    a = inpt[:inpt.find("(")]
    w1 = inpt[inpt.find("(")+1:inpt.find(",")]
    w2 = inpt[inpt.find(",")+1:inpt.find(")")].strip()
    spl = inpt[inpt.find(":")+1:]
    b = spl[:spl.find("(")]
    v = spl[spl.find("(")+1:spl.find(",")]

    cat1 = ar.get_category([w1, v]) # Get category w1 and v belong to, and print it
    print(f"{bcolors.HEADER}Identified category of '{w1}' and '{v}': {cat1}{bcolors.ENDC}")
    
    cat = ar.get_category([w2]) # Get category w2 belongs to, and print it
    print(f"{bcolors.HEADER}Identified category of '{w2}': {cat}{bcolors.ENDC}\n")
    
    s = ar.norm_distance(w1, v, cat1, verbose = verbose) # Compute distance between precisiated values of w1 and v
    
    res = ar.norm_getmostrelatedword(w2, cat, s)
    
    w2p = ar.precisiation(w2, cat)
    resp = ar.precisiation(res[1], cat)
    
    print(f"\n{bcolors.BOLD}If {a} is {w1} and {w2} then {b}, which is {v}, is {bcolors.FAIL}{res[1]}{bcolors.ENDC}.\n")
    print(f"Details:\nDistance between {res[1]}* and {w2}*: {bcolors.WARNING}{abs(w2p-resp)}{bcolors.ENDC}\nDistance between {w1}* and {v}*: {bcolors.WARNING}{s}{bcolors.ENDC}\n")
    
    ar.display_precisiated_values(w2, w2p, res[1], resp)

else:
    print("no match")
