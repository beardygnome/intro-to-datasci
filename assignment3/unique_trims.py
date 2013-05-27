import MapReduce
import sys

"""
DNA Nucleotide Trimmimg Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # seq_id: the sequence identifier
    # nucleotides: the sequence of nucleotides

    seq_id = record[0]
    nucleotides = record[1]

    mr.emit_intermediate(nucleotides[:-10], 1)


def reducer(key, occurrence_list):
    # key: trimmed nucleotide string
    # ocurrence_list: list of ocuurence counts

    mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
