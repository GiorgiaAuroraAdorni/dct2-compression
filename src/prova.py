from util import get_file, extract_columns, reshape_columns
from my_plot import comparison_result

import numpy as np

input = get_file("results", "dct2_comparison.2.csv")

columns = extract_columns(input)

n = columns["n"][-1:]
my = columns["my"][-4:]
orig = columns["orig"][-4:]

reshaped_columns = reshape_columns(columns)

my_mean = []
orig_mean = []

for i in range(len(reshaped_columns["iteration"])):
    my_mean.append(np.mean(reshaped_columns["my"][i, :]))
    orig_mean.append(np.mean(reshaped_columns["orig"][i, :]))

size = np.append(reshaped_columns["n"][:, 0], np.array([n]))
my_mean.append(np.mean(my))
orig_mean.append(np.mean(orig))

comparison_result(size, [my_mean, orig_mean], ["my", "orig"], "DCT2", "results/prova_iteration.pdf")
