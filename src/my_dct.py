import numpy as np


def dct(f, axis=-1):
    """
    Compute the Discrete Cosine Transform over the specified axis.

    :param     f: The input array.
    :param  axis: Axis along which the DCT is computed. The default is over the last axis.
    :return    c: The computed DCT.
    """

    # Size of the input along the specified axis.
    n = f.shape[axis]

    # Create two vectors containing the integers from 0 to n-1.
    i = k = np.arange(n)

    # Compute the x-axis coordinate of the f function.
    x = (2 * i + 1) / (2 * n)

    # Compute the outer product of x and kπ, obtaining the nxn matrix that will
    # form the argument of the cosine.
    arg = np.multiply.outer(x, k * np.pi)

    # Normalization factors.
    alpha = np.where(k == 0, 1 / np.sqrt(n), np.sqrt(2 / n))

    # The orthonormal DCT basis.
    w = alpha * np.cos(arg)

    # Compute the convolution between the input array and the DCT basis.
    # The output contains the amplitude coefficient for every frequency.
    c = np.tensordot(f, w, axes=(axis, 0))

    # `axis` becomes the last dimension in the output of `np.tensordot`.
    # Move it back to its original position so that the output shape matches
    # the input shape.
    c = np.moveaxis(c, -1, axis)

    return c


def dctn(array, axes=None):
    """
    Compute the multidimensional Discrete Cosine Transform over the specified axes.

    :param array: The input array
    :param axes: Axes along which the DCT is computed. The default is over all axes.
    :return: The computed DCT
    """

    # Axes along which the DCT is computed. The default is over all axes.
    if axes is None:
        axes = range(array.ndim)

    # Apply the 1D DCT to each axis in sequence.
    for axis in axes:
        array = dct(array, axis=axis)

    return array
