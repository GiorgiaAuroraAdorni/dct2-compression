from scipy.fftpack import dct, dctn
import my_dct as my
import numpy as np
import pprint

pp = pprint.PrettyPrinter(indent=4)

block = np.array([[231, 32, 233, 161, 24, 71, 140, 245],
                  [247, 40, 248, 245, 124, 204, 36, 107],
                  [234, 202, 245, 167, 9, 217, 239, 173],
                  [193, 190, 100, 167, 43, 180, 8, 70],
                  [11, 24, 210, 177, 81, 243, 8, 112],
                  [97, 195, 203, 47, 125, 114, 165, 181],
                  [193, 70, 174, 167, 41, 30, 127, 245],
                  [87, 149, 57, 192, 65, 129, 178, 228]])

# block = np.random.randint(0, 255, size=(4, 5, 6))

pp.pprint("Test matrix:")
pp.pprint(block)

original2 = dctn(block, norm="ortho")
custom2 = my.dctn(block)
are_close2 = np.allclose(original2, custom2)

pp.pprint("Official DCT2:")
pp.pprint(original2)
print()
pp.pprint("My DCT2:")
pp.pprint(custom2)
print()
pp.pprint("All values are almost equal?")
pp.pprint(are_close2)
print()
print()

############################

pp.pprint("Test vector:")
pp.pprint(block[0])


original1 = dct(block[0], axis=0, norm="ortho")
custom1 = my.dct(block[0], axis=0)
are_close1 = np.allclose(original1, custom1)

pp.pprint("Official DCT1:")
pp.pprint(original1)
print()
pp.pprint("My DCT1:")
pp.pprint(custom1)
print()
pp.pprint("All values are almost equal?")
pp.pprint(are_close1)
print()
print()


# for axis in range(block.ndim):
#   original = dct(block, axis=axis, norm="ortho")
#   custom = my.dct(block, axis=axis)
#   are_close = np.allclose(original, custom)

  # print("Official 1D DCT, axis", axis)
  # print(original)
  # print()
  # print("My 1D DCT, axis", axis)
  # print(custom)
  # print()
  # print("All values are almost equal?", are_close)
  # print()

