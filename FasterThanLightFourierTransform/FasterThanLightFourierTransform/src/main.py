import util

import numpy as np
import scipy.fftpack as fft

OUTPUT_DCT = 0
OUTPUT_MASK = 1
OUTPUT_COMPRESSED_DCT = 2
OUTPUT_COMPRESSED_IMAGE = 3


def compress_image(image, window, cutoff, output=OUTPUT_COMPRESSED_IMAGE):
    gray = util.im2gray(image)

    cropped = util.crop(gray, window)
    shaped = util.blockshaped(cropped, window)

    dct = fft.dctn(shaped, axes=[1, 2], type=2, norm='ortho')
    compressed, mask = util.compress(dct, cutoff)
    idct = fft.idctn(compressed, axes=[1, 2], type=2, norm='ortho')

    info = np.iinfo(image.dtype)
    to_range = (info.min, info.max)
    
    if output == OUTPUT_DCT:
        out = dct
        from_range = (out.min(), out.max())
    elif output == OUTPUT_MASK:
        out = mask
        from_range = (out.min(), out.max()) #FIXME: min == max should map to 0
    elif output == OUTPUT_COMPRESSED_DCT:
        out = compressed
        from_range = (out.min(), out.max())
    elif output == OUTPUT_COMPRESSED_IMAGE:
        out = idct
        from_range = to_range # No interpolation needed, just clipping
    else:
        raise ValueError("Invalid value for 'output' parameter.")
    
    normalized = np.interp(out, from_range, to_range)
    converted = np.round(normalized).astype(image.dtype)

    if output == OUTPUT_MASK:
        result = converted
    else:
        result = util.unblockshaped(converted, cropped.shape)

    return result
