import util

import numpy as np
import scipy.fftpack as fft


def compress_image(image, window, cutoff):
    gray = util.im2gray(image)

    cropped = util.crop(gray, window)
    shaped = util.blockshaped(cropped, window)

    dct = fft.dctn(shaped, axes=[1, 2], type=2, norm='ortho')
    compressed = util.compress(dct, cutoff)
    idct = fft.idctn(compressed, axes=[1, 2], type=2, norm='ortho')

    range = np.iinfo(image.dtype)
    normalized = np.clip(np.round(idct), range.min, range.max).astype(image.dtype)
    result = util.unblockshaped(normalized, cropped.shape)

    return result
