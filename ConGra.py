#!/user/bin/env python

import numpy as np
import networkx as nx
from scipy import linalg
from copy import deepcopy
from scipy.linalg import expm

def evolution_operator(G, t):
    adj = np.array(nx.adjacency_matrix(G).todense())
    #get the adjacency matrix
    U = expm( 1j * adj * t)
    # U indicates the quantum evolution operator
    return U

def ConGra(G, t):
    diameter = nx.diameter(G) #the diameter of network G
    values = np.empty(len(G))
    final = np.zeros(len(G))
    evo_outcome = evolution_operator(G, t)
    eigenvalues = linalg.eigvals(evo_outcome)
    E_Gcompleted = np.sum(eigenvalues.real ** 2) #total energy
    for u in G:
        GG = deepcopy(G)
        GG.remove_node(u)
        temp = linalg.eigvals(evolution_operator(GG, t))
        temp = np.sum(temp.real ** 2)
        values[u - 1] = E_Gcompleted - temp
    for u in G:
        for v in G[u]:
            a = nx.shortest_path_length(G, u, v)
            if a <= diameter/2 and u != v:
                final[u-1] += (values[u - 1] * values[v - 1]) / (a ** 2)
    return final