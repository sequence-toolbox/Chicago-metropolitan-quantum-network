from statistics import mean
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.size'] = 15
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd



def get_data(filename):
    df = pd.read_csv(filename)
    return df["Throughput"]

def draw():
    d1 = ['cavity_cooperativity_50', 'cavity_cooperativity_100', 'cavity_cooperativity_500']
    d2 = ["efficiency_0.01", "efficiency_0.10", "efficiency_0.50", "efficiency_0.75"]
    d3 = ['memo_freq']
    d4 = ['2000']
    width = 0.17
    pattern = ['*', '\\\\', '.', 'x']

    for i, _d2 in enumerate(d2):
        tps = []
        for _d1 in d1:
            for _d3 in d3:
                for _d4 in d4:
                    filename = '%s/%s/%s/%s/request.csv' % (_d1, _d2, _d3, _d4)
                    data = get_data(filename)
                    tps.append(mean(data))
        if _d2 == "efficiency_0.01":
            print(tps)
        plt.bar(np.arange(len(d1)) + width * i, tps, width=width, hatch=pattern[i])

    plt.yscale("log")
    plt.ylabel("Average per Flow Throughput (pair / sec)")
    plt.xlabel("Atom-cavity cooperativity")
    plt.xticks(np.arange(3) + 0.25, ['50', '100', '500'])
    plt.legend(["e=0.01", "e=0.10", "e=0.50", "e=0.75"], bbox_to_anchor=(-0.1, 1.02, 1.2, .102), loc='lower left', ncol=4, mode="expand", borderaxespad=0)
    plt.grid(axis='y', which='minor', alpha=0.2)
    # plt.show()
    plt.savefig("fig8.pdf", bbox_inches='tight')


if __name__ == "__main__":
    draw()
