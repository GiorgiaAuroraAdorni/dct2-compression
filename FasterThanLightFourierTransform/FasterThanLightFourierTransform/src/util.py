import numpy as np


def im2gray(image):
    if image.ndim == 3 and image.shape[2] in [3, 4]:
        out = 0.2126 * image[:, :, 0] + 0.7152 * image[:, :, 1] + 0.0722 * image[:, :, 2]
        
        return out.astype(image.dtype)
    else:
        return image
    

def crop(arr, n):
    """
    Crop array so that all its dimensions are multiples of n
    """
    h, w = arr.shape

    h -= h % n
    w -= w % n

    return arr[:h, :w]


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
    # Take the last two dimensions of the input
    block_rows, block_cols = array.shape[-2:]

    j = np.arange(block_rows)
    k = np.arange(block_cols)

    # Select the elements where j + k ≥ threshold
    mask = np.less.outer(j, -k + threshold)

    # Zero them out
    output = np.where(mask, array, 0)

    return output, mask
