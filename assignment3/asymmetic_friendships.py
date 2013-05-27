import MapReduce
import sys

"""
Social Network Asymmetric Friendships Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # personA: the person identifier
    # personB: the friend identifier

    person = record[0]
    friend = record[1]

    # output each friendship both ways
    # for symmetric friendships, there will be two keys, one for each direction
    # so for asymmetric friendships, there will only be one
    mr.emit_intermediate((person, friend), 1)
    mr.emit_intermediate((friend, person), 1)


def reducer(key, friend_count_list):
    # key: friendship identifier, (person, their friend)
    # friend_count_list: list of friend counts

    # for symmetric friendships, there will be two keys, one for each direction
    # so for asymmetric friendships, there will only be one
    if sum(friend_count_list) == 1:
        mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
