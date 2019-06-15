import matplotlib.pyplot as plt
import numpy as np


def comparison_result(x, y_set, labels, title, filename):

    for i in range(len(y_set)):
        plt.plot(x, y_set[i], 'o-', linewidth=3, markersize=8, label=labels[i])

    y = x * np.log(x) / 100000
    y_square = (x ** 2) * np.log(x) / 100000000
    y_cube = (x ** 3) * np.log(x) / 100000000000

    plt.plot(x, y, '--', linewidth=3, markersize=8, label="n")
    plt.plot(x, y_square, '--', linewidth=3, markersize=8, label="n^2")
    plt.plot(x, y_cube, '--', linewidth=3, markersize=8, label="n^3")

    plt.yscale('log')

    plt.xlabel("size", fontsize=12)
    plt.ylabel("time (sec)", fontsize=12)

    plt.title(title, weight='bold', fontsize=14, y=1.05)
    plt.legend()

    plt.savefig(filename)
    plt.show()
