import numpy as np


def im2gray(image):
    # FIXME: preserve alpha
    if len(image.shape) == 3 and image.shape[2] in [3, 4]:
        out = 0.2126 * image[:, :, 0] + 0.7152 * image[:, :, 1] + 0.0722 * image[:, :, 2]
        
        return out.astype(image.dtype)
    else:
        return image
    

def blockshaped(arr, n):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n sub-blocks with
    each sub-block preserving the "physical" layout of arr.
    """
    h, w = arr.shape

    assert h % n == 0, "{} rows is not evenly divisible by {}".format(h, n)
    assert w % n == 0, "{} cols is not evenly divisible by {}".format(w, n)

    return (arr.reshape(h//n, n, -1, n)
               .swapaxes(1, 2)
               .reshape(-1, n, n))


def unblockshaped(arr, shape):
    """
    Return an array of shape (h, w) where
    h * w = arr.size

    If arr is of shape (n, nrows, ncols), n sub-blocks of shape (nrows, ncols),
    then the returned array preserves the "physical" layout of the sub-blocks.
    """
    h, w = shape
    n, nrows, ncols = arr.shape

    return (arr.reshape(h//nrows, -1, nrows, ncols)
               .swapaxes(1, 2)
               .reshape(h, w))


def compress(array, threshold):
### TODO: measure the performance improvement 😂
    (_, blockRows, blockCols) = array.shape

    for j in range(0, blockRows):
        for k in range(0, blockCols):
            if j + k >= threshold:
                array[:, j, k] = 0

#    c[threshold:] = 0

    # FIXME: c is modified in place
    return array
