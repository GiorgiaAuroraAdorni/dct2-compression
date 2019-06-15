import numpy as np


def dct(array, axis=-1):
    n = array.shape[axis]

    i = k = np.arange(n)

    foo = (2*i + 1) / (2*n)
    bar = k * np.pi
    asd = np.multiply.outer(foo, bar)

    alpha = np.where(k == 0, 1 / np.sqrt(n), np.sqrt(2 / n))
    basis = alpha * np.cos(asd)

    dct = np.tensordot(array, basis, axes=(axis, 0))

    # np.tensordot
    baz = np.moveaxis(dct, -1, axis)

    return baz


def dctn(array, axes=None):
    # Axes along which the DCT is computed. The default is over all axes.
    if axes is None:
        axes = range(array.ndim)

    for axis in axes:
        array = dct(array, axis=axis)

    return array
