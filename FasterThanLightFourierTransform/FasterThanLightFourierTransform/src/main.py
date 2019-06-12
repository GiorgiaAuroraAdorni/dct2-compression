import util

import numpy as np
from scipy.fftpack import dctn, idctn


def compress_image(image, window, cutoff):
    shaped = util.blockshaped(image, window)

    result_array = np.zeros((shaped.shape))

    for i in range(shaped.shape[0]):
        # discrete cosine transform
        c = dctn(shaped[i], type=2, norm='ortho')

        compressed = util.compression(c, cutoff)

        # inverse discrete cosine transform
        ff = idctn(compressed, type=2, norm='ortho')

        # normalize idct
        normalized_ff = np.clip(ff, 0, 255)

        result_array[i] = ff

    final = util.unblockshaped(result_array, image.shape[0], image.shape[1])

    return final
