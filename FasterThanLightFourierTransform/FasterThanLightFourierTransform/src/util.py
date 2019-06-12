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


def arr2im(data, fname):
    out = Image.new('RGB', data.shape[1::-1])
    out.putdata(map(tuple, data.reshape(-1, 3)))
    out.save(fname)


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
               .swapaxes(1,2)
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
               .swapaxes(1,2)
               .reshape(h, w))


# Functions to go from image to frequency-image and back

im2freq = lambda data: fp.rfft(fp.rfft(data, axis=0), axis=1)
freq2im = lambda f: fp.irfft(fp.irfft(f, axis=1), axis=0)

###############

wd_path = "/Users/Giorgia/FtlFT"

filename = wd_path + "/images/barbara.bmp"
outfile = wd_path + "/images/freq.png"

img = Image.open(filename).convert('L')
windowsize = 8 # not work if not a divisor of the original shape
threshold = 4

# plt.imshow(img, cmap='gray', vmin=0, vmax=255)
# plt.show()

data = load_image(img)

# freq = im2freq(data)
# back = freq2im(freq)

# # Make sure the forward and backward transforms work!
# assert(np.allclose(data, back))

shaped = blockshaped(data, windowsize)

iterator = int(len(data) / windowsize)

result_array = np.array([])
list_result = []

for i in range(iterator):
    # discrete cosine transform
    c = dctn(shaped[i], type=2, norm='ortho')

    # compression
    (blockRows, blockCols) = shaped[i].shape

    for j in range(0, blockRows - 1):
        for k in range(0, blockCols - 1):
            if j + k >= threshold:
                c[j, k] = 0

    # inverse discrete cosine transform
    ff = idctn(c, type=2, norm='ortho')

    # normalize idct
    ff = np.round(ff)
    for index, value in np.ndenumerate(ff):
        if value < 0:
            ff[index] = 0
        elif value > 255:
            ff[index] = 255

    list_result.append(ff)
    # np.vstack([result_array, ff])
    # result_array = result_array.append([ff])
    if result_array.size == 0:
        result_array = np.array([ff])
    # else:
        # result_array = np.append(result_array, ff, axis=0)

# result_array = np.array([result_array])
# final = unblockshaped(result_array, data.shape[0], data.shape[1])
#
# print(shaped[1])
# print("\n \n okk \n \n")
# print(shaped)
#
# print("\n \n okk \n \n")
#

print(result_array)

plt.imshow(result_array, cmap='gray', vmin=0, vmax=255)
plt.show()



