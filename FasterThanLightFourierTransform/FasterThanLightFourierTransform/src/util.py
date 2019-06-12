import numpy as np
from scipy.fftpack import dctn, idctn


def blockshaped(arr, n):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    assert h % n == 0, "{} rows is not evenly divisble by {}".format(h, n)
    assert w % n == 0, "{} cols is not evenly divisble by {}".format(w, n)
    return (arr.reshape(h//n, n, -1, n)
               .swapaxes(1, 2)
               .reshape(-1, n, n))


def unblockshaped(arr, h, w):
    """
    Return an array of shape (h, w) where
    h * w = arr.size

    If arr is of shape (n, nrows, ncols), n sublocks of shape (nrows, ncols),
    then the returned array preserves the "physical" layout of the sublocks.
    """
    n, nrows, ncols = arr.shape
    return (arr.reshape(h//nrows, -1, nrows, ncols)
               .swapaxes(1, 2)
               .reshape(h, w))


def compression(c, threshold):
    (blockRows, blockCols) = c.shape

    for j in range(0, blockRows - 1):
        for k in range(0, blockCols - 1):
            if j + k >= threshold:
                c[j, k] = 0

    return c