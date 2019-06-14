import matplotlib.pyplot as plt


def comparison_result(x, y_set, labels, title, filename):

    for i in range(len(y_set)):
        plt.plot(x, y_set[i], 'o-', linewidth=3, markersize=8, label=labels[i])

    plt.yscale('log')

    plt.xlabel("size", fontsize=12)
    plt.ylabel("time (sec)", fontsize=12)

    plt.title(title, weight='bold', fontsize=14, y=1.05)
    plt.legend()

    plt.savefig(filename)
    plt.show()
