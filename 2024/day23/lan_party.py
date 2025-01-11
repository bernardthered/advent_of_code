# Solution to
# https://adventofcode.com/2024/day/23


from itertools import combinations
import os
import networkx as nx
import matplotlib.pyplot as plt
from sympy import pretty_print


def read_input(filenum):
    G = nx.Graph()
    script_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_path, f"input_{filenum}.txt")) as inputfile:
        for line in inputfile.readlines():
            node1, node2 = line.strip().split("-")
            G.add_edge(node1, node2)
    return G


def count_sets_of_three(G):
    sets = set()
    for node in G.nodes:
        if not node.startswith("t"):
            continue
        for adjacent_node_1, adjacent_node_2 in combinations(G[node], 2):
            if adjacent_node_1 in G[adjacent_node_2]:
                sets.add(tuple(sorted([node, adjacent_node_1, adjacent_node_2])))
    return len(sets)


def part1():
    G = read_input(2)
    print(count_sets_of_three(G))
    # nx.draw_shell(G)
    # plt.show()


def bron_kerbosch(candidate_clique: set, available_vertices: set, exclude: set, G):
    max_max_clique = set()
    if not available_vertices and not exclude:
        # The candidate_clique is a maximum clique!
        return candidate_clique
    while available_vertices:
        vertex = available_vertices.pop()
        max_clique = bron_kerbosch(
            candidate_clique | set([vertex]),
            available_vertices & set(G[vertex]),
            exclude & set(G[vertex]),
            G,
        )
        if len(max_clique) > len(max_max_clique):
            max_max_clique = max_clique
        exclude.add(vertex)
    return max_max_clique


def part2():
    G = read_input(2)
    max_max_clique = bron_kerbosch(set(), set(G.nodes), set(), G)
    print("Password:", ",".join(sorted(max_max_clique)))


if __name__ == "__main__":
    part2()
