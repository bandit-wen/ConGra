import csv
import networkx as nx
import math
from copy import deepcopy

def dictionaryConstract(vol):
    # construct the sequence obtained from the ConGra and the other comparison approaches.
    node_id, measured_value = [], []
    with open('dophin-result-001.csv', 'r') as f:
        csvFile = csv.reader(f)
        for item in csvFile:
            node_id.append(int(item[0]))
            measured_value.append(float(item[vol]))
    return dict(zip(node_id, measured_value))

def conGravRobust(G, vol):
    result = dictionaryConstract(vol)
    sorted_data = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    GforQuantum = deepcopy(G)
    numNodes = nx.number_of_nodes(G)
    robustnessList = []
    for index in range(10):
        pianduan = math.floor(numNodes * 0.1)
        if index == 9:
            robustnessList.append(0)
        else:
            sortedList = list(sorted_data.keys())
            tempnode = sortedList[:pianduan]
            GforQuantum.remove_nodes_from(tempnode)
            sorted_data = {key: sorted_data[key] for key in sorted_data if key not in tempnode}
            C = max(nx.connected_components(GforQuantum), key=len, default=0)
            C = list(C)
            robustnessList.append(len(C) / numNodes)
    return robustnessList
