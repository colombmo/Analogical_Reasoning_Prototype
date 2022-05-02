import json
from thesaurus_v2 import Word


class SynDB:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}

        try:
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        except:
            with open(self.filename, 'w') as outfile:
                json.dump(self.data, outfile)
    
    # Retrieve synonyms from the cache (self.data) if present, otherwise get them from thesaurus.com
    def retrieve_syn(self, w, ant = [], rel=[1, 2, 3]):
        if w in self.data:
            return self.data[w]
        else:
            syns = Word(w).synonyms("all", relevance=rel)
            self.data[w] = syns
            with open(self.filename, 'w') as outfile:
                json.dump(self.data, outfile)
            return syns
