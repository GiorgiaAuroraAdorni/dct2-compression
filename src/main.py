from scipy.fftpack import dctn
import numpy as np
import time

from my_plot import comparison_result
from my_dct import dct2

times_my_dct = np.zeros(1500)
times_original_dct = np.zeros(1500)
size = np.arange(2, times_my_dct.shape[0]+2, dtype="int32")

for N in range(2, times_my_dct.shape[0]+2):
    matrix = np.random.randint(0, 255, size=(N, N))

    # my dct
    start_time = time.time()
    dct2(matrix)
    end_time = time.time()

    times_my_dct[N-2] = end_time - start_time     # time taken

    # original dct
    start_time = time.time()
    dctn(matrix, type=2, norm='ortho')
    end_time = time.time()

    times_original_dct[N-2] = end_time - start_time     # time taken


comparison_result(size, [times_original_dct, times_my_dct], ["my_dct2", "original_dct2"], "DCT2", "results/dct2_comparison.pdf")


############ TEST

# block = np.array([[231, 32, 233, 161, 24, 71, 140, 245],
#                   [247, 40, 248, 245, 124, 204, 36, 107],
#                   [234, 202, 245, 167, 9, 217, 239, 173],
#                   [193, 190, 100, 167, 43, 180, 8, 70],
#                   [11, 24, 210, 177, 81, 243, 8, 112],
#                   [97, 195, 203, 47, 125, 114, 165, 181],
#                   [193, 70, 174, 167, 41, 30, 127, 245],
#                   [87, 149, 57, 192, 65, 129, 178, 228]])
#
# print("dct2 official\n", dctn(block, type=2, norm='ortho'))
# print("\n")
# print("my dct2\n", dct2(block))
# print("\n")
# print("\n")
#
# print("dct1 official\n", dct(block, norm="ortho"))
# print("\n")
# print("my dct1\n", dct1(block))
