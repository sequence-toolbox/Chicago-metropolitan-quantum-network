from collections import deque, defaultdict
from statistics import mean, stdev

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.size'] = 20


def bar_request_num():
    width = 0.6
    cases = ['starlight', 'uneven_memory']
    y_data = []
    y_error = []
    for i, root in enumerate(cases):
        request_num = []
        for j in range(10):
            filename = "%s/%d/request.csv" % (root, j)
            df = pd.read_csv(filename)
            data = []
            for index, row in df.iterrows():
                if row["End_time"] < 1e15:
                    data.append(row)
            request_num.append(len(data))
        y_data.append(mean(request_num))
        y_error.append(stdev(request_num))
    print("completed requests ", y_data)
    plt.bar(np.arange(2), y_data, width, yerr=y_error)
    ticks = np.arange(2)
    labels = ["Even", "Weighted"]
    plt.xticks(ticks, labels)
    plt.ylabel("Completed Requests")
    plt.savefig("fig11b.pdf", bbox_inches='tight')

    # plt.show()



def get_avg_ent_num(root):
    datas = []
    for j in range(10):
        filename = "%s/%d/request.csv" % (root, j)
        df = pd.read_csv(filename)
        nums = round(df['Throughput'] * (df['End_time'] - df['Start_time']) / 1e12)
        print(filename, sum(nums))
        datas.append(sum(nums))
    return datas

def bar_distributed_entangle():
    width = 0.6
    cases = ['starlight', 'uneven_memory']
    y_data = []
    y_error = []
    for i, root in enumerate(cases):
        net_tp = np.array(get_avg_ent_num(root))  / 1000
        y_data.append(mean(net_tp))
        y_error.append(stdev(net_tp))
    print("net throughput", y_data)
    plt.bar(np.arange(2), y_data, width=width, yerr=y_error)
    ticks = np.arange(2)
    labels = ["Even", "Weighted"]
    plt.xticks(ticks, labels)
    plt.ylabel("Aggregate Throughput (pairs / sec)")
    plt.savefig("fig11a.pdf", bbox_inches='tight')
    # plt.show()


def single_graph(data):
    data = sorted(data, key=lambda x:x[0])
    x, y = [0], [0]
    stack = deque()
    for d in data:
        s_t, e_t, n = d
        while stack and stack[0][0] <= s_t:
            x.append(stack[0][0])
            y.append(y[-1])
            x.append(stack[0][0])
            y.append(y[-1] - stack[0][1])
            stack.pop(0)
        x.append(s_t)
        y.append(y[-1])
        x.append(s_t)
        y.append(y[-1]+n)
        stack.append([e_t, n])
        stack = sorted(stack,key=lambda x:x[0])

    while stack:
        x.append(stack[0][0])
        y.append(y[-1])
        x.append(stack[0][0])
        y.append(y[-1] - stack[0][1])
        stack.pop(0)

    return x, y

def usage_rate_with_time(filename, memory_dist, node, color, fig_name):
    df = pd.read_csv(filename)
    datas = defaultdict(lambda : [])
    for index, row in df.iterrows():
        datas[row["Node"]].append([row["Start_time"]/1e12, row["End_time"]/1e12, row["Memory_size"]])

    x, y = single_graph(datas[node])
    y = [n / memory_dist[node] * 100 for n in y]
    print(node, "avg usage rate", mean(y))
    plt.plot(x, y, color=color)
    plt.axhline(100)
    plt.fill_between(x, y, color=color)
    plt.xlabel("Time (sec)")
    plt.ylabel("Memory Usage Rate (%)")
    plt.savefig("%s.pdf" % (fig_name), bbox_inches='tight')
    # plt.show()

    full_used_times = []
    for X, Y in zip(x, y):
        if Y > 80:
            full_used_times.append(X)

    agg_full_used_time = 0
    for i in range(0, len(full_used_times), 2):
        agg_full_used_time += full_used_times[i + 1] - full_used_times[i]

    plt.clf()


if __name__ == "__main__":
    fig = plt.figure(figsize=(5, 6))
    bar_request_num()
    fig = plt.figure(figsize=(5, 6))
    bar_distributed_entangle()

    fig = plt.figure(figsize=(6, 6))

    filename1 = 'starlight/0/memory_usage.csv'
    memory_dist = {"Argonne_1": 50, "Argonne_2": 50, "Argonne_3": 50, "Fermilab_1": 50,
                   "Fermilab_2": 50, "StarLight": 50, "NU": 50, "UChicago_PME": 50, "UChicago_HC": 50}
    for node, fig_name in zip(["Argonne_3", "StarLight"], ['fig10a', 'fig10b']):
        usage_rate_with_time(filename1, memory_dist, node, '#1776B6', fig_name)

    filename2 = 'uneven_memory/0/memory_usage.csv'
    memory_dist = {"Argonne_1": 103, "Argonne_2": 25, "Argonne_3": 24, "Fermilab_1": 67,
                   "Fermilab_2": 24, "StarLight": 91, "NU": 25, "UChicago_PME": 67, "UChicago_HC": 24}
    for node, fig_name in zip(["Argonne_3", "StarLight"], ['fig10c', 'fig10d']):
        usage_rate_with_time(filename2, memory_dist, node, '#FF8300', fig_name)
