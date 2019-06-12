import main

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt


def load_image(img):
    img.load()
    data = np.array(img, dtype="int32")
    return data


def save_image(npdata, outfilename):
    img = Image.fromarray(np.asarray(np.clip(npdata, 0, 255), dtype="uint8"), "L")
    img.save(outfilename)


##########################


wd_path = "/Users/Giorgia/FtlFT"

filename = wd_path + "/images/barbara.bmp"
outfile = wd_path + "/images/freq.png"

img = Image.open(filename).convert('L')
windowsize = 8 # not work if not a divisor of the original shape
threshold = 2

data = load_image(img)

final = main.compress_image(data, windowsize, threshold)

plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray', vmin=0, vmax=255)

plt.subplot(1, 2, 2)
plt.imshow(final, cmap='gray', vmin=0, vmax=255)

plt.show()

################## TEST ##################

prova_blocco = np.array([[231,    32,   233,   161,    24,    71,   140,   245],
                            [247,    40,   248,   245,   124,   204,    36,   107],
                            [234,   202,   245,   167,     9,   217,   239,   173],
                            [193,   190,   100,   167,    43,   180,     8,    70],
                            [ 11,    24,   210,   177,    81,   243,     8,   112],
                            [ 97,   195,   203,    47,   125,   114,   165,   181],
                            [193,    70,   174,   167,    41,    30,   127,   245],
                            [ 87,   149,    57,   192,    65,   129,   178,   228]])



prova_c = dctn(prova_blocco, type=2, norm='ortho')

prova_compressed = compression(prova_c)

prova_ff = idctn(prova_compressed, type=2, norm='ortho')

prova_normalized_ff = normalize(prova_ff)
