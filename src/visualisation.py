import matplotlib.pyplot as plt
import numpy as np


def comparison_result(x, y_set, labels, title, filename):
    
    plt.figure(figsize=(16,9))

    for i in range(len(y_set)):
        plt.plot(x, y_set[i], 'o-', linewidth=3, markersize=8, label=labels[i])

    # y_square = (x ** 2) * np.log(x) / 100000000
    # y_cube = (x ** 3) / 10000000000

    # y_square = (x ** 2) * np.log(x) / 100000000
    # y_cube = (x ** 3) / 10000000000

    # plt.plot(x, y_square, '--', linewidth=3, markersize=8, label="n^2*log(n)")
    # plt.plot(x, y_cube, '--', linewidth=3, markersize=8, label="n^3")

    plt.yscale('log')
    plt.xscale('log')

    m = min(y_set[0][0], y_set[1][0])
    plt.ylim(bottom=m/10)
    plt.xlabel("size", fontsize=12)
    plt.ylabel("time (sec)", fontsize=12)

    plt.title(title, weight='bold', fontsize=14, y=1.05)
    plt.legend()

    plt.savefig(filename)
    plt.show()
