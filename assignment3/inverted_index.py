from __future__ import absolute_import, division, print_function, unicode_literals

import MapReduce
import sys

"""
Inverted Index Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # doc_id: document identifier
    # text: document contents

    doc_id = record[0]
    text = record[1]
    words = text.split()

    for w in words:
        #print w, doc_id
        mr.emit_intermediate(w, doc_id)

def reducer(key, doc_list):
    # key: word
    # doc_list: list of doc_ids

    result = []

    for doc in doc_list:
        if not doc in result:
            result.append(doc)

    mr.emit((key, result))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
