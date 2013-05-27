import MapReduce
import sys

"""
Social Network Friend Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # personA: the person identifier
    # personB: the friend identifier

    person = record[0]
    friend = record[1]

    mr.emit_intermediate(person, 1)


def reducer(key, friend_count_list):
    # key: person identifier
    # friend_count_list: list of friend counts

    mr.emit((key, sum(friend_count_list)))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
