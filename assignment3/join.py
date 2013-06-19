from __future__ import absolute_import, division, print_function, unicode_literals

import MapReduce
import sys

"""
Relational Join Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # table: table identifier
    # order_id: order identifier

    table = record[0]
    order_id = record[1]

    mr.emit_intermediate(order_id, record)


def reducer(key, record_list):
    # key: order_id
    # record_list: list of records

    result_list = [order + item for order in record_list if order[0] == "order"
                    for item in record_list if item[0] == "line_item"]

    for result in result_list:
        mr.emit(result)

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
