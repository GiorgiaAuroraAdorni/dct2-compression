from collections import defaultdict
import numpy as np
import csv
import os


def get_file(directory, filename):
    out = ""

    # Iterate over all the entries
    for file in os.listdir(directory):
        if file.endswith(filename):
            # Store full path
            out = (os.path.join(directory, file))

    return out


def extract_columns(directory):
    columns = defaultdict(list)

    with open(directory, 'r') as f:
        reader = csv.DictReader(f)  # read rows into a dictionary format
        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            for (k, v) in row.items():  # go over each column name and value
                if k != 'name':
                    columns[k].append(float(v))  # append the value into the appropriate list based on column name k
                else:
                    columns[k].append(v)

    return columns


def reshape_columns(columns):

    for el in columns:
        col = np.array(columns[el])
        col = col[:-4]
        col = np.reshape(col, (-1, 10))
        columns[el] = col

    return columns
