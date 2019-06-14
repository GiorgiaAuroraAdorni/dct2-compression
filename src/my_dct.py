import numpy as np
from scipy.fftpack import dctn, dct


def my_dct(vec):
    size = vec.size
    c = np.zeros(shape=size)

    # to avoid iteration
    alpha = np.pad([1 / np.sqrt(size)], (0, size - 1), 'constant', constant_values=(np.sqrt(2 / size)))

    for j in range(size):

        # alternatively:
        # alpha = 1 if j != 0 else np.sqrt(0.5)
        # alpha = np.sqrt(2 / size) * alpha

        # another alternative:
        # alpha = (1.0 / size)**(1.0 / 2.0)
        # alpha = (2.0 / size) ** (1.0 / 2.0)

        sum = 0.0

        for index, val in np.ndenumerate(vec):
            i = index[0]
            sum += val * np.cos(np.pi * j * (2 * i + 1) / (2 * size))

            c[j] = alpha[j] * sum
            # c[j] = alpha * sum

    return c


def dct1(c):
    first_dct = np.apply_along_axis(my_dct, 1, c)

    return first_dct


def dct2(matrix):
    # Applies DCT1 on the first axises and after to the second (transpose)
    second_dct = np.apply_along_axis(my_dct, 1, np.apply_along_axis(my_dct, 0, matrix))

    return second_dct
