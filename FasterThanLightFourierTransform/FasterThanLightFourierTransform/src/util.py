from PIL import Image
import numpy as np
import scipy.fftpack as fp
from matplotlib import pyplot as plt
from scipy.fftpack import dctn, idctn


def load_image(img):
    img.load()
    data = np.array(img, dtype="int32")
    return data


def save_image(npdata, outfilename):
    img = Image.fromarray(np.asarray(np.clip(npdata, 0, 255), dtype="uint8"), "L")
    img.save(outfilename)


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


def compression(c):
    (blockRows, blockCols) = c.shape

    for j in range(0, blockRows - 1):
        for k in range(0, blockCols - 1):
            if j + k >= threshold:
                c[j, k] = 0

    return c


def normalize(idct):
    idct = np.round(idct)

    for index, value in np.ndenumerate(idct):
        if value < 0:
            idct[index] = 0
        elif value > 255:
            idct[index] = 255

    return idct

##########################

wd_path = "/Users/Giorgia/FtlFT"

filename = wd_path + "/images/barbara.bmp"
outfile = wd_path + "/images/freq.png"

img = Image.open(filename).convert('L')
windowsize = 8 # not work if not a divisor of the original shape
threshold = 2

data = load_image(img)

shaped = blockshaped(data, windowsize)

result_array = np.zeros((shaped.shape))

for i in range(shaped.shape[0]):
    # discrete cosine transform
    c = dctn(shaped[i], type=2, norm='ortho')

    compressed = compression(c)

    # inverse discrete cosine transform
    ff = idctn(compressed, type=2, norm='ortho')

    # normalize idct
    normalized_ff = normalize(ff)

    result_array[i] = ff

final = unblockshaped(result_array, data.shape[0], data.shape[1])

plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray', vmin=0, vmax=255)

plt.subplot(1, 2, 2)
plt.imshow(final, cmap='gray', vmin=0, vmax=255)

plt.show()



