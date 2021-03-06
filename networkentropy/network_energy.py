import numpy as np
import networkx as nx
import scipy
import scipy.stats

from itertools import product

def get_randic_matrix(G):
    """
    Computes the Randić matrix of a graph

    Elements of the Randić matrix are defined as follows:

               0 if v=w
    R(v,w) =   1/sqrt(D(v)*D(w)) if (v,w) in E(G)
               0 otherwise

    :param G: input graph
    :return: NumPy matrix
    """

    D = nx.degree(G)

    randic_values = [1 / np.sqrt(D[v] * D[w]) if G.has_edge(v, w) else 0 for (v, w) in product(G.nodes, G.nodes)]
    randic_matrix = np.matrix(randic_values).reshape(G.number_of_nodes(), G.number_of_nodes())

    return randic_matrix


def get_randic_index(G):
    """
    Computes the Randić index of a graph

    Randić index is the sum of non-zero elements of the Randić matrix of a graph

    :param G: input graph
    :return: float: Randić index of a graph
    """

    D = nx.degree(G)

    randic_values = [1 / np.sqrt(D[v] * D[w]) if G.has_edge(v, w) else 0 for (v, w) in product(G.nodes, G.nodes)]
    randic_index = sum(randic_values)

    return randic_index


def get_randic_energy(G):
    """
    Computes the Randić energy of a graph

    Randić energy is the sum of all absolute eigenvalues of the Randić matrix of a graph

    :param G: input graph
    :return: float: Randić energy of a graph
    """

    R = get_randic_matrix(G)
    randic_energy = np.abs(scipy.linalg.eigvals(R).real).sum()

    return randic_energy


def get_laplacian_energy(G):
    """
    Computes the energy of the Laplacian of a graph

    :param G: input graph
    :return: float: Laplacian energy of a graph
    """

    L = nx.laplacian_matrix(G).todense()
    laplacian_energy = np.abs(scipy.linalg.eigvals(L).real).sum()

    return laplacian_energy


def get_graph_energy(G):
    """
    Computes the energy of the adjacency matrix of a graph

    :param G: input graph
    :return: float: energy of the adjacency matrix of a graph
    """

    M = nx.adjacency_matrix(G).todense()
    graph_energy = np.abs(scipy.linalg.eigvals(M).real).sum()

    return graph_energy

def get_distance_matrix(G):
    """
    Computes the distance matrix of a graph

    :param G: input graph
    :return: matrix with elements representing shortest paths between nodes
    """

    distance_matrix = np.zeros(G.number_of_nodes() * G.number_of_nodes()).\
        reshape(G.number_of_nodes(), G.number_of_nodes())
    distance_values = [(x,y,d[y]) for (x,d) in nx.all_pairs_dijkstra_path_length(G) for y in d.keys()]

    for (x,y,d) in distance_values:
        distance_matrix[x,y] = d

    return distance_matrix


def get_distance_energy(G):
    """
    Computes the distance energy of a graph

    Distance energy is the sum of all absolute eigenvalues of the distance matrix of a graph

    :param G: input graph
    :return: float: distance energy of a graph
    """

    D = get_distance_matrix(G)
    distance_energy = np.abs(scipy.linalg.eigvals(D).real).sum()

    return distance_energy

# TODO add the retrieval of spectra from a graph
# TODO fix the computation of the Laplacian energy by subtracting 2m/n