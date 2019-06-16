import numpy as np
from scipy.fftpack import dct, dctn

import my_dct as my

block = np.array([[231, 32, 233, 161, 24, 71, 140, 245],
                  [247, 40, 248, 245, 124, 204, 36, 107],
                  [234, 202, 245, 167, 9, 217, 239, 173],
                  [193, 190, 100, 167, 43, 180, 8, 70],
                  [11, 24, 210, 177, 81, 243, 8, 112],
                  [97, 195, 203, 47, 125, 114, 165, 181],
                  [193, 70, 174, 167, 41, 30, 127, 245],
                  [87, 149, 57, 192, 65, 129, 178, 228]])

# block = np.random.randint(0, 255, size=(4, 5, 6))

for axis in range(block.ndim):
    original = dct(block, axis=axis, norm="ortho")
    custom = my.dct(block, axis=axis)
    are_close = np.allclose(original, custom)

    print("Official 1D DCT, axis", axis)
    print(original)
    print()
    print("My 1D DCT, axis", axis)
    print(custom)
    print()
    print("All values are almost equal?", are_close)
    print()

original = dctn(block, norm="ortho")
custom = my.dctn(block)
are_close = np.allclose(original, custom)

print("Official ND DCT")
print(original)
print()
print("My ND DCT")
print(custom)
print()
print("All values are almost equal?", are_close)
print()
