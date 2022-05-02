import syn_retriever as sr
import numpy as np
import itertools

syns_relx = sr.SynDB("all_relevance.txt")

print("Synonyms loaded successfully")

	
# Return a tuple with the index of the maximum element in a multidimensional array, and a tuple with the number of
# common synonyms and the total number of synonyms
def max2d(lst_tuples):
    divided = np.array([[tup[0] / tup[1] if tup[1] != 0 else 0 for tup in lst] for lst in lst_tuples])
    maxid = np.where(divided == np.amax(divided))

    return ((maxid[0][0], maxid[1][0]), lst_tuples[maxid[0][0]][maxid[1][0]])

# Function to count the number of common elements in two lists
def count_overlaps(l1, l2):
    return len(set(l1) & set(l2))


# Function to compute similarity between two words, based on the percentage of common synonyms

def sim(w1, w2, ant=[]):
    global syns_relx

    syns1, syns2 = syns_relx.retrieve_syn(w1, ant=ant), syns_relx.retrieve_syn(w2, ant=ant)

    syns1 = [s + [w1] for s in syns1]
    syns2 = [s + [w2] for s in syns2]

    return [[(count_overlaps(syn1, syn2), (len(syn1) + len(syn2)))
             for syn2 in syns2] for syn1 in syns1]


# Helper function to flatten 2d list

def flat(lst):
    return [x for l in lst for x in l]


# Level 2 similarity of words
def sim_lvl2(w1, w2):
    global syns_relx # Not so elegant

    # Get all synonyms for all meanings
    syn1 = syns_relx.retrieve_syn(w1)
    syn2 = syns_relx.retrieve_syn(w2)

    comb = list(itertools.product(syn1, syn2))

    # This part here is to reduce execution time:
    # select from the lists of synonyms, the meanings with the highest number of overlaps
    # Then use only these two meanings to compute the overlaps over the second-order synonyms
    if len(syn1) > 1 and len(syn2) > 1:
        r = [count_overlaps(cp[0], cp[1]) for cp in comb]

        if max(r)>0:
            id = np.argmax(r)
            syn1 = [syn1[id//len(syn2)]]
            syn2 = [syn2[id%len(syn2)]]

            comb = itertools.product(syn1, syn2)

    # END of code optimization part

    res_lvl2 = max2d([[np.sum([np.sum([max2d(sim(wi, wj))[1] for wj in c[0]], axis=0) for wi in c[1]], axis=0) for c in comb]])[1]

    return 2 * res_lvl2[0] / res_lvl2[1] if res_lvl2[1] != 0 else 0

# The following is a potentially faster solution, but
# TODO: results to be checked: count the total number of possible meanings of all adjectives,
#   compute overlaps between full list of level 2 synonyms, and use number of meanings to normalize the total number of
#   overlaps to the number of meanings

'''
    meanings = 0

    # Get all synonyms for all meanings
    syn1 = syns_relx.retrieve_syn(w1)
    syn2 = syns_relx.retrieve_syn(w2)

    meanings += len(syn1)
    meanings += len(syn2)

    synsl2_w1 = [syns_relx.retrieve_syn(s) for l in syn1 for s in l]
    synsl2_w2 = [syns_relx.retrieve_syn(s) for l in syn2 for s in l]

    for a in synsl2_w1:
        meanings += len(a)

    for a in synsl2_w2:
        meanings += len(a)

    ssf_w1 = [z for l in synsl2_w1 for s in l for z in s]
    ssf_w2 = [z for l in synsl2_w2 for s in l for z in s]

    return count_overlaps(ssf_w1, ssf_w2)*meanings/(len(ssf_w1)+ len(ssf_w2))
'''


# Level 1 similarity of words

def sim_lvl1(w1, w2):

    res_lvl1 = max2d(sim(w1, w2))[1]

    return 2 * res_lvl1[0] / res_lvl1[1] if res_lvl1[1] != 0 else 0

