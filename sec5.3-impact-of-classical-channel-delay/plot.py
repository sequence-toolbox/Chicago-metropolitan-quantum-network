import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean, stdev
import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.size'] = 15


def draw():
    width = 0.35
    d1 = ['cavity_cooperativity_500']
    d2 = ["efficiency_0.75"]
    d3 = ['memo_freq']
    d4 = ['200', '2000', '20000']
    pattern = ['\\', '/']

    for d in d1:
        for e in d2:
            for i, root in enumerate(['regular', 'low_delay']):
                tps = []
                for _d3 in d3:
                    for freq in d4:
                        filename = '%s/%s/%s/%s/%s/request.csv' % (root, d, e, _d3, freq)
                        df = pd.read_csv(filename)
                        tps.append(mean(df['Throughput']))

                plt.xticks(np.arange(3) + 0.25, d4)
                plt.xlabel("Memory Frequency (Hz)")
                plt.bar(np.arange(3)+i*width, tps, width, hatch=pattern[i])

            plt.ylabel("Average per Flow  Throughput (pair / sec)")
            plt.legend(["regular delay", "low delay"])
            plt.savefig("fig9.pdf", bbox_inches='tight')
            # plt.show()


if __name__ == "__main__":
    draw()
