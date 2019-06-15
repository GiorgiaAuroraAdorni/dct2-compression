from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import csv
import os


def comparison_result(x, y_set, labels, title, filename):

    for i in range(len(y_set)):
        plt.plot(x, y_set[i], 'o-', linewidth=3, markersize=8, label=labels[i])

    y = x * np.log(x) / 100000
    y_square = (x ** 2) * np.log(x) / 100000000
    y_cube = (x ** 3) * np.log(x) / 100000000000

    plt.plot(x, y, '--', linewidth=3, markersize=8, label="n")
    plt.plot(x, y_square, '--', linewidth=3, markersize=8, label="n^2")
    plt.plot(x, y_cube, '--', linewidth=3, markersize=8, label="n^3")

    plt.yscale('log')

    m = min(y_set[0][0], y_set[1][0])
    plt.ylim(bottom=m/10)
    plt.xlabel("size", fontsize=12)
    plt.ylabel("time (sec)", fontsize=12)

    plt.title(title, weight='bold', fontsize=14, y=1.05)
    plt.legend()

    plt.savefig(filename)
    plt.show()


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


input = get_file("results", "dct2_comparison.2.csv")

columns = extract_columns(input)

for el in columns:
    col = np.array(columns[el])
    col = col[:-4]
    col = np.reshape(col, (-1, 10))

    columns[el] = col

my_mean = []
orig_mean = []

for i in range(len(columns["iteration"])):
    my_mean.append(np.mean(columns["my"][i, :]))
    orig_mean.append(np.mean(columns["orig"][i, :]))

comparison_result(columns["n"][:, 0], [my_mean, orig_mean], ["my", "orig"], "DCT2", "results/prova_iteratio.pdf")

