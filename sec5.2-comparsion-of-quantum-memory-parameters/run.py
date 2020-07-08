import pandas as pd
from numpy.random import seed
from sequence.app.random_request import RandomRequestApp
from sequence.components.optical_channel import ClassicalChannel
from sequence.kernel.timeline import Timeline
from sequence.topology.node import QuantumRouter, MiddleNode
from sequence.topology.topology import Topology

def program(log_path, MEMO_FREQ, MEMO_EXPIRE, MEMO_EFFICIENCY, MEMO_FIDELITY, DETECTOR_EFFICIENCY, DETECTOR_COUNT_RATE, DETECTOR_RESOLUTION, ATTENUATION, QC_FREQ, SWAP_SUCC_PROB, SWAP_DEGRADATION):
    print(log_path, "running")
    # Experiment params and config
    network_config_file = "starlight.json"
    runtime = 1e15

    seed(1)
    tl = Timeline(runtime)
    network_topo = Topology("network_topo", tl)
    network_topo.load_config(network_config_file)

    # set memory parameters
    for name, node in network_topo.nodes.items():
        if isinstance(node, QuantumRouter):
            node.memory_array.update_memory_params("frequency", MEMO_FREQ)
            node.memory_array.update_memory_params("coherence_time", MEMO_EXPIRE)
            node.memory_array.update_memory_params("efficiency", MEMO_EFFICIENCY)
            node.memory_array.update_memory_params("raw_fidelity", MEMO_FIDELITY)

    # set detector parameters
    for name, node in network_topo.nodes.items():
        if isinstance(node, MiddleNode):
            node.bsm.update_detectors_params("efficiency", DETECTOR_EFFICIENCY)
            node.bsm.update_detectors_params("count_rate", DETECTOR_COUNT_RATE)
            node.bsm.update_detectors_params("time_resolution", DETECTOR_RESOLUTION)

    # set quantum channel parameters
    for qc in network_topo.qchannels:
        qc.attenuation = ATTENUATION
        qc.frequency = QC_FREQ

    # set entanglement swapping parameters
    for name, node in network_topo.nodes.items():
        if isinstance(node, QuantumRouter):
            node.network_manager.protocol_stack[1].set_swapping_success_rate(SWAP_SUCC_PROB)
            node.network_manager.protocol_stack[1].set_swapping_degradation(SWAP_DEGRADATION)

    nodes_name = []
    for name, node in network_topo.nodes.items():
        if isinstance(node, QuantumRouter):
            nodes_name.append(name)

    apps = []
    for i, name in enumerate(nodes_name):
        app_node_name = name
        others = nodes_name[:]
        others.remove(app_node_name)
        app = RandomRequestApp(network_topo.nodes[app_node_name], others, i)
        apps.append(app)
        app.start()

    tl.init()
    tl.run()

    initiators = []
    responders = []
    start_times = []
    end_times = []
    memory_sizes = []
    fidelities = []
    wait_times = []
    throughputs = []
    for node in network_topo.nodes.values():
        if isinstance(node, QuantumRouter):
            initiator = node.name
            reserves = node.app.reserves
            _wait_times = node.app.get_wait_time()
            _throughputs = node.app.get_throughput()
            min_size = min(len(reserves), len(_wait_times), len(_throughputs))
            reserves = reserves[:min_size]
            _wait_times = _wait_times[:min_size]
            _throughputs = _throughputs[:min_size]
            for reservation, wait_time, throughput in zip(reserves, _wait_times, _throughputs):
                responder, s_t, e_t, size, fidelity = reservation
                initiators.append(initiator)
                responders.append(responder)
                start_times.append(s_t)
                end_times.append(e_t)
                memory_sizes.append(size)
                fidelities.append(fidelity)
                wait_times.append(wait_time)
                throughputs.append(throughput)
    log = {"Initiator": initiators, "Responder": responders, "Start_time": start_times, "End_time": end_times,
           "Memory_size": memory_sizes, "Fidelity": fidelities, "Wait_time": wait_times, "Throughput": throughputs}

    import os
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    df = pd.DataFrame(log)
    df.to_csv(log_path+"/request.csv")

    print(log_path, "Done")


if __name__ == "__main__":
    from cavity_vs_fidelity import get_fidelity_by_efficiency
    import multiprocessing
    pool = multiprocessing.Pool()

    for C in [50, 100, 500]:
        for e in [0.01, 0.1, 0.5, 0.75]:
            fidelity = get_fidelity_by_efficiency(C)
            for freq in [2000]:
                path = "cavity_cooperativity_%d/efficiency_%.2f/memo_freq/%d" % (C, e, freq)
                pool.apply_async(program, args=(path, freq, 1.3, e, fidelity, 0.8, 5e7, 100, 0.0002, 1e11, 0.64, 0.99))
    pool.close()
    pool.join()

