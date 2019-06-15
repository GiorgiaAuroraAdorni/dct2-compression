from scipy.fftpack import dctn
import numpy as np
import time

from my_plot import comparison_result
import my_dct as my

iterations = 10
count = 14

times_my_dct = np.zeros(count)
times_original_dct = np.zeros(count)

indices = np.arange(count)
sizes = 2 ** (indices + 1)

print("iteration,n,my,orig")

for i, n in zip(indices, sizes):
    for iteration in range(iterations):
        matrix = np.random.randint(0, 255, size=(n, n))

        # my dct
        start = time.time()
        a = my.dctn(matrix)
        end = time.time()

        times_my_dct[i] = end - start           # time taken

        # original dct
        start = time.time()
        b = dctn(matrix, type=2, norm='ortho')
        end = time.time()

        times_original_dct[i] = end - start     # time taken

        are_close = np.allclose(a, b)

        print("{},{},{},{}".format(iteration, n, times_my_dct[i], times_original_dct[i]))


comparison_result(sizes, [times_original_dct, times_my_dct], ["original_dct2", "my_dct2"], "DCT2", "results/dct2_comparison.pdf")
