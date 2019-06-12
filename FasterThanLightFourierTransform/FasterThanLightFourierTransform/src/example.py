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
