import MapReduce
import sys

"""
Sparse Matrix Multiplication Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # matrix: the matrix identifier
    # row_num: the row number
    # col_num: the column number
    # value: the cell value

    matrix = record[0]
    row_num = record[1]
    col_num = record[2]
    value = record[3]

    for i in range(5):
        if matrix == "a":
            mr.emit_intermediate((row_num, i), ("a", col_num, value))
        elif matrix == "b":
            mr.emit_intermediate((i, col_num), ("b", row_num, value))



def reducer(key, values_list):
    # key: matrix cell reference
    # values_list: list of all values for the dot product

    a = {item[1]: item[2] for item in values_list if item[0] == "a"}
    b = {item[1]: item[2] for item in values_list if item[0] == "b"}

    result = sum([a[i] * b[i] for i in range(5) if i in a and i in b])


    if result != 0:
        mr.emit((key[0], key[1], result))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
