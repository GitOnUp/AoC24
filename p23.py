import re
from collections import deque, defaultdict


def read_input():
    with open("p23.input.txt", "r") as f:
        for line in f.readlines():
            link = line.strip().split('-')
            yield link[0], link[1]


def build_graph():
    graph = defaultdict(set)
    for link in read_input():
        l1, l2 = link
        graph[l1].add(l2)
        graph[l2].add(l1)
    return graph


def find_cycles(graph: {str: {str}}):
    seen_cycles = set()
    for starting_node in graph:
        paths = deque([[starting_node]])
        while paths:
            path = paths.popleft()
            if len(path) == 3:
                if starting_node in graph[path[-1]]:
                    seen_cycles.add(",".join(sorted(path)))
            else:
                for next_node in graph[path[-1]]:
                    paths.append(path + [next_node])
    return seen_cycles


if __name__ == "__main__":
    total = 0
    for cycle in find_cycles(build_graph()):
        if "t" in (cycle[0], cycle[3], cycle[6]):
            total += 1
    print(total)

